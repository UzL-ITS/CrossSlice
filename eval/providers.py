"""
Provider abstraction for the agent experiments: one `Session` interface over
the Anthropic Messages API and any OpenAI-compatible chat endpoint (used for
OpenRouter). A model is named `<provider>:<model-id>`:

    anthropic:claude-opus-4-8
    openrouter:qwen/qwen3-coder-30b-a3b-instruct

Each session owns its provider-specific message history; the agent loop only
sees normalized `Turn` objects (thinking, text, tool calls, stop reason, usage).
"""

import asyncio
import json
import os
import re
from dataclasses import dataclass, field

OPENROUTER_BASE = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# OpenAI-style `reasoning.effort` accepts low/medium/high; map the Anthropic
# ladder onto it for OpenRouter models that support reasoning.
_EFFORT_OPENAI = {"low": "low", "medium": "medium", "high": "high",
                  "xhigh": "high", "max": "high"}


@dataclass
class Usage:
    inp: int = 0
    out: int = 0
    cache_read: int = 0
    cost: float | None = None      # USD, when the provider reports it


@dataclass
class Turn:
    thinking: str
    text: str
    tool_calls: list                # [(id, name, args_dict)]
    stop_reason: str                # tool_use | end_turn | max_tokens | other
    usage: Usage
    raw: object = field(default=None, repr=False)


def parse_model(spec: str):
    """'openrouter:qwen/x' -> ('openrouter', 'qwen/x'); bare id -> anthropic."""
    if ":" in spec:
        p, m = spec.split(":", 1)
        return p.strip().lower(), m.strip()
    return "anthropic", spec.strip()


def slug(spec: str) -> str:
    _, m = parse_model(spec)
    return re.sub(r"[^A-Za-z0-9.]+", "-", m).strip("-")


def make_session(model_spec, system, first_user, effort="high", max_tokens=12000,
                 provider_order=None, provider_ignore=None):
    provider, model = parse_model(model_spec)
    if provider == "anthropic":
        return AnthropicSession(model, system, first_user, effort, max_tokens)
    if provider in ("openrouter", "openai"):
        return OpenAISession(model, system, first_user, effort, max_tokens,
                             base_url=OPENROUTER_BASE if provider == "openrouter" else None,
                             provider_order=provider_order, provider_ignore=provider_ignore)
    raise ValueError(f"unknown provider '{provider}' in {model_spec}")


# ------------------------------- Anthropic ---------------------------------

# First-party prices, USD per million tokens: input, output, cache read, cache
# write (5-minute TTL) — platform.claude.com/pricing as of 2026-10. Haiku 5.5:
# the rate for prompts up to 100K tokens. Unknown models record no cost.
ANTHROPIC_PRICES = {
    "claude-opus-5-5":   (4.00, 20.00, 0.20, 5.00),
    "claude-sonnet-5-5": (2.00, 10.00, 0.20, 2.50),
    "claude-haiku-5-5":  (0.10, 0.50, 0.01, 0.125),
    "claude-opus-5":     (5.00, 25.00, 0.50, 6.25),
    "claude-opus-4-8":   (5.00, 25.00, 0.50, 6.25),
    "claude-sonnet-5":   (2.00, 10.00, 0.20, 2.50),
}
# models that reject a forced tool_choice (`any` / a named tool): the loop has
# already asked for the submission in the prompt, so `auto` is sent instead
_NO_FORCED_TOOL = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-fable", "claude-mythos")
# server-side refusal fallback (beta): "default" lets Anthropic pick the
# substitute model by refusal category; "" disables it. A run records which
# model served each turn, so a fallback never goes unnoticed in the results.
ANTHROPIC_FALLBACKS = os.environ.get("EVAL_ANTHROPIC_FALLBACKS", "default")


def anthropic_cost(model, inp, out, cache_read, cache_write):
    p = ANTHROPIC_PRICES.get(model)
    if not p:
        return None
    return (inp * p[0] + out * p[1] + cache_read * p[2] + cache_write * p[3]) / 1e6


class AnthropicSession:
    """Messages API with adaptive thinking, effort, tools, prompt caching of
    the growing conversation (top-level cache_control), and the server-side
    refusal fallback. `Usage.inp` is the FULL prompt (uncached + cache reads +
    cache writes), so budgets and token counts mean the same with and without
    caching and across providers; `Usage.cache_read` says how much of it was
    served from the cache."""

    def __init__(self, model, system, first_user, effort, max_tokens, fallbacks=None):
        import anthropic
        self.client = anthropic.AsyncAnthropic()
        self.model, self.system = model, system
        self.effort, self.max_tokens = effort, max_tokens
        self.messages = [{"role": "user", "content": first_user}]
        self.fallbacks = ANTHROPIC_FALLBACKS if fallbacks is None else fallbacks
        self.served_models = {}       # model -> turns it produced (fallbacks show up here)
        self.refusals = []            # (turn, stop_details category)
        self.cache_write = 0

    def _extras(self):
        body = {"cache_control": {"type": "ephemeral"}}
        headers = {}
        if self.fallbacks:
            body["fallbacks"] = self.fallbacks
            headers["anthropic-beta"] = "server-side-fallback-2026-07-01"
        return body, headers

    @staticmethod
    def _usage(resp, served):
        u = resp.usage
        cr = getattr(u, "cache_read_input_tokens", 0) or 0
        cw = getattr(u, "cache_creation_input_tokens", 0) or 0
        return Usage(u.input_tokens + cr + cw, u.output_tokens, cr,
                     anthropic_cost(served, u.input_tokens, u.output_tokens, cr, cw)), cw

    async def step(self, tools, force_tool=None) -> Turn:
        body, headers = self._extras()
        kwargs = dict(
            model=self.model, max_tokens=self.max_tokens, system=self.system,
            thinking={"type": "adaptive", "display": "summarized"},
            tools=tools, messages=self.messages,
            output_config={"effort": self.effort},
            extra_body=body, extra_headers=headers,
        )
        if force_tool and not self.model.startswith(_NO_FORCED_TOOL):
            kwargs["tool_choice"] = {"type": "tool", "name": force_tool}
        resp = await self.client.messages.create(**kwargs)
        if resp.content:  # a refusal before any output has none; keep the history valid
            self.messages.append({"role": "assistant", "content": resp.content})
        served = getattr(resp, "model", None) or self.model
        self.served_models[served] = self.served_models.get(served, 0) + 1
        if resp.stop_reason == "refusal":
            details = getattr(resp, "stop_details", None) or (getattr(resp, "model_extra", None) or {}).get("stop_details")
            cat = getattr(details, "category", None) if details is not None and not isinstance(details, dict) \
                else (details or {}).get("category")
            self.refusals.append((len(self.messages), cat))
        thinking = " ".join(b.thinking for b in resp.content
                            if b.type == "thinking" and b.thinking)
        text = " ".join(b.text for b in resp.content if b.type == "text")
        calls = [(b.id, b.name, dict(b.input)) for b in resp.content if b.type == "tool_use"]
        usage, cw = self._usage(resp, served)
        self.cache_write += cw
        return Turn(thinking, text, calls, resp.stop_reason, usage, resp)

    def add_tool_results(self, results):
        self.messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": cid, "content": text}
            for cid, _name, text in results]})

    def add_user(self, text):
        self.messages.append({"role": "user", "content": text})

    async def one_shot(self, system, user, schema, max_tokens=None):
        """Single structured answer (JSON matching `schema`)."""
        resp = await self.client.messages.create(
            model=self.model, max_tokens=max_tokens or self.max_tokens, system=system,
            thinking={"type": "adaptive", "display": "summarized"},
            messages=[{"role": "user", "content": user}],
            output_config={"format": {"type": "json_schema", "schema": schema},
                           "effort": self.effort},
        )
        thinking = " ".join(b.thinking for b in resp.content
                            if b.type == "thinking" and b.thinking)
        text = next((b.text for b in resp.content if b.type == "text"), "{}")
        served = getattr(resp, "model", None) or self.model
        usage, _ = self._usage(resp, served)
        return (json.loads(text) if resp.stop_reason != "refusal" else {}), thinking, usage


# --------------------------- OpenAI-compatible -----------------------------

def lenient_json(text):
    """Parse model-produced JSON that may be fenced, truncated or trailing:
    returns a dict, or {"_raw": text} when nothing sensible can be recovered."""
    if isinstance(text, dict):
        return text
    t = (text or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    for cand in (t, t[: t.rfind("}") + 1] if "}" in t else "", t + '"}', t + "}", t + '"]}'):
        if not cand:
            continue
        try:
            d = json.loads(cand)
            if isinstance(d, dict):
                return d
        except json.JSONDecodeError:
            continue
    pairs = re.findall(r'"([A-Za-z_]\w*)"\s*:\s*"((?:[^"\\]|\\.)*)', t)
    if pairs:
        d = {}
        for k, v in pairs:
            try:
                d[k] = json.loads(f'"{v}"')
            except json.JSONDecodeError:
                d[k] = v
        d["_partial"] = True
        return d
    return {"_raw": text}


_XML_FN = re.compile(r"<function=([\w\-]+)>(.*?)</function>", re.S)
_XML_PARAM = re.compile(r"<parameter=([\w\-]+)>\s*(.*?)\s*</parameter>", re.S)
_TOOLCALL_JSON = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.S)


def _coerce(v):
    v = v.strip()
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v


def parse_text_tool_calls(text, known_names):
    """Tool calls a model wrote into its message text instead of the
    tool_calls field (Qwen/Llama-style XML or <tool_call> JSON) — some
    providers fail to parse these. Returns [(name, args)]."""
    calls = []
    if not text:
        return calls
    for m in _XML_FN.finditer(text):
        name = m.group(1)
        if name in known_names:
            calls.append((name, {k: _coerce(v) for k, v in _XML_PARAM.findall(m.group(2))}))
    for m in _TOOLCALL_JSON.finditer(text):
        d = lenient_json(m.group(1))
        name = d.get("name")
        if name in known_names:
            args = d.get("arguments", d.get("parameters", {}))
            if isinstance(args, str):
                args = lenient_json(args)
            calls.append((name, args if isinstance(args, dict) else {}))
    if not calls and text.strip().startswith("{"):
        d = lenient_json(text)
        name = d.get("name")
        if name in known_names:
            args = d.get("arguments", d.get("parameters", {}))
            calls.append((name, args if isinstance(args, dict) else {}))
    return calls


def _oa_tools(tools):
    return [{"type": "function", "function": {
        "name": t["name"], "description": t.get("description", ""),
        "parameters": t["input_schema"]}} for t in tools]


class OpenAISession:
    """Chat Completions with function calling (OpenRouter or any compatible
    endpoint). Reasoning is requested via OpenRouter's `reasoning` field and
    read back from `message.reasoning` when the model returns it."""

    def __init__(self, model, system, first_user, effort, max_tokens, base_url=None,
                 provider_order=None, provider_ignore=None):
        import openai
        key = os.environ.get("OPENROUTER_API_KEY") if base_url else os.environ.get("OPENAI_API_KEY")
        if not key:
            raise SystemExit("OPENROUTER_API_KEY (or OPENAI_API_KEY) is not set — "
                             "export it or add it to .env")
        self.client = openai.AsyncOpenAI(base_url=base_url, api_key=key,
                                         default_headers={"HTTP-Referer": "commit-context-enrichment",
                                                          "X-Title": "commit-context-enrichment eval"})
        self.model, self.effort, self.max_tokens = model, effort, max_tokens
        self.messages = [{"role": "system", "content": system},
                         {"role": "user", "content": first_user}]
        # require_parameters: only route to providers that support every
        # parameter we send (tools!) — without it OpenRouter may pick a
        # provider that silently drops tool calls.
        routing = {"require_parameters": True}
        if provider_order:            # pin: try these providers, in order, only
            routing["order"] = list(provider_order)
            routing["allow_fallbacks"] = False
        ignore = set(provider_ignore or []) | _BAD_PROVIDERS.get(model, set())
        if ignore:
            routing["ignore"] = sorted(ignore)
        self._extra = {"usage": {"include": True}, "provider": routing}
        # only ask for reasoning when the model advertises it — with
        # require_parameters an unsupported parameter yields "no endpoints"
        if base_url is None or _supports(model, "reasoning"):
            self._extra["reasoning"] = {"effort": _EFFORT_OPENAI.get(effort, "high")}
        self.providers_seen = {}
        self.empty_from = {}          # provider -> empty responses seen
        self.text_tool_calls = 0      # tool calls recovered from message text
        self._txt_ids = 0
        self._pending_assistant = None

    async def _create(self, messages, tools=None, tool_choice=None, max_tokens=None):
        kwargs = dict(model=self.model, messages=messages,
                      max_tokens=max_tokens or self.max_tokens, extra_body=self._extra)
        if tools:
            kwargs["tools"] = _oa_tools(tools)
        if tool_choice:
            kwargs["tool_choice"] = tool_choice
        last = None
        for attempt in range(5):
            try:
                resp = await self.client.chat.completions.create(**kwargs)
                if not getattr(resp, "choices", None):
                    # OpenRouter can answer 200 with an error body and no
                    # choices (upstream provider failure): retry, and exclude
                    # the provider that failed when it is named
                    err = getattr(resp, "error", None) or (resp.model_extra or {}).get("error")
                    bad = getattr(resp, "provider", None)
                    if bad:
                        routing = dict(self._extra.get("provider", {}))
                        routing["ignore"] = sorted(set(routing.get("ignore", [])) | {bad})
                        self._extra = {**self._extra, "provider": routing}
                        kwargs["extra_body"] = self._extra
                    raise RuntimeError(f"empty choices from {bad}: {str(err)[:200]}")
                return resp
            except Exception as e:  # rate limits / transient provider errors
                last = e
                status = getattr(e, "status_code", None)
                text = str(e).lower()
                if "reasoning" in self._extra and (
                        "reasoning" in text or "requested parameters" in text):
                    # provider rejects the reasoning parameter: drop it and retry
                    self._extra = {k: v for k, v in self._extra.items() if k != "reasoning"}
                    kwargs["extra_body"] = self._extra
                    continue
                if status in (400, 401, 403, 404):
                    raise
                await asyncio.sleep(2 ** attempt)
        raise last

    async def step(self, tools, force_tool=None) -> Turn:
        choice_arg = ({"type": "function", "function": {"name": force_tool}}
                      if force_tool else ("auto" if tools else None))
        resp = await self._create(self.messages, tools, choice_arg)
        msg = resp.choices[0].message
        # Some providers return an empty message (no content, no tool calls)
        # while still billing completion tokens — the model's tool call was
        # emitted in a format the provider did not parse. Exclude that
        # provider (for this model, for the rest of the run) and retry.
        for _attempt in range(3):
            if msg.content or msg.tool_calls or \
                    (getattr(resp.usage, "completion_tokens", 0) or 0) == 0:
                break
            bad = getattr(resp, "provider", None)
            if bad:
                _BAD_PROVIDERS.setdefault(self.model, set()).add(bad)
                self.empty_from[bad] = self.empty_from.get(bad, 0) + 1
                routing = dict(self._extra.get("provider", {}))
                routing["ignore"] = sorted(set(routing.get("ignore", [])) | {bad})
                self._extra = {**self._extra, "provider": routing}
            resp = await self._create(self.messages, tools, choice_arg)
            msg = resp.choices[0].message
        prov = getattr(resp, "provider", None)
        if prov:
            self.providers_seen[prov] = self.providers_seen.get(prov, 0) + 1
        assistant = {"role": "assistant", "content": msg.content or ""}
        calls = []
        if msg.tool_calls:
            assistant["tool_calls"] = []
            for tc in msg.tool_calls:
                args = lenient_json(tc.function.arguments or "{}")
                calls.append((tc.id, tc.function.name, args))
                # history gets normalized JSON: a model's malformed arguments
                # (e.g. two objects concatenated) would otherwise be echoed
                # back and rejected by the provider on the next turn
                clean = {k: v for k, v in args.items() if not k.startswith("_")}
                assistant["tool_calls"].append({
                    "id": tc.id, "type": "function",
                    "function": {"name": tc.function.name,
                                 "arguments": json.dumps(clean)}})
        elif msg.content and tools:
            # the model wrote its tool call as text (XML / <tool_call> JSON)
            # and the provider did not parse it: recover it ourselves
            known = {t["name"] for t in tools}
            parsed = parse_text_tool_calls(msg.content, known)
            if parsed:
                self.text_tool_calls += len(parsed)
                assistant["tool_calls"] = []
                assistant["content"] = _XML_FN.sub("", _TOOLCALL_JSON.sub("", msg.content)).strip()
                for name, args in parsed:
                    cid = f"txt{self._txt_ids}"
                    self._txt_ids += 1
                    calls.append((cid, name, args))
                    assistant["tool_calls"].append({
                        "id": cid, "type": "function",
                        "function": {"name": name, "arguments": json.dumps(args)}})
        # keep the model's reasoning in history when the provider returns it
        reasoning = getattr(msg, "reasoning", None) or ""
        if reasoning:
            assistant["reasoning"] = reasoning
        if calls:
            # deferred: add_tool_results() writes one single-call assistant
            # turn per call (some providers reject parallel tool calls, and
            # routing can switch providers mid-conversation)
            self._pending_assistant = assistant
        else:
            self.messages.append(assistant)
        fr = resp.choices[0].finish_reason
        stop = ("tool_use" if calls else
                "max_tokens" if fr == "length" else
                "end_turn" if fr in ("stop", None) else fr)
        u = resp.usage
        usage = Usage(getattr(u, "prompt_tokens", 0) or 0,
                      getattr(u, "completion_tokens", 0) or 0,
                      (getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", 0) or 0),
                      getattr(u, "cost", None))
        return Turn(reasoning, msg.content or "", calls, stop, usage, resp)

    def add_tool_results(self, results):
        pending = getattr(self, "_pending_assistant", None)
        self._pending_assistant = None
        by_id = {tc["id"]: tc for tc in (pending or {}).get("tool_calls", [])}
        first = True
        for cid, name, text in results:
            tc = by_id.get(cid) or {"id": cid, "type": "function",
                                    "function": {"name": name, "arguments": "{}"}}
            self.messages.append({
                "role": "assistant",
                "content": (pending or {}).get("content", "") if first else "",
                **({"reasoning": pending["reasoning"]}
                   if first and pending and pending.get("reasoning") else {}),
                "tool_calls": [tc]})
            first = False
            self.messages.append({"role": "tool", "tool_call_id": cid,
                                  "name": name, "content": text})

    def add_user(self, text):
        self.messages.append({"role": "user", "content": text})

    async def one_shot(self, system, user, schema, max_tokens=None):
        """Structured answer via a forced function call carrying the schema —
        the most portable way to get schema-valid JSON from mixed providers."""
        tool = {"name": "answer", "description": "Return the answer.", "input_schema": schema}
        resp = await self._create(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            [tool], {"type": "function", "function": {"name": "answer"}}, max_tokens)
        msg = resp.choices[0].message
        if msg.tool_calls:
            data = lenient_json(msg.tool_calls[0].function.arguments or "{}")
        else:  # model ignored the forced call: try to parse JSON from the text
            m = re.search(r"\{.*\}", msg.content or "", re.S)
            data = lenient_json(m.group(0)) if m else {}
        u = resp.usage
        return data, getattr(msg, "reasoning", "") or "", Usage(
            getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0,
            0, getattr(u, "cost", None))


_MODEL_PARAMS: dict = {}
# providers that returned an empty-but-billed message for a model in this
# process: excluded from routing for the rest of the run (learned per model)
_BAD_PROVIDERS: dict = {}


def _supports(model: str, param: str) -> bool:
    """Whether an OpenRouter model advertises `param` in supported_parameters
    (public models endpoint, fetched once; unknown models -> False)."""
    if not _MODEL_PARAMS:
        try:
            import urllib.request
            with urllib.request.urlopen(OPENROUTER_BASE + "/models", timeout=30) as r:
                for m in json.load(r)["data"]:
                    _MODEL_PARAMS[m["id"]] = set(m.get("supported_parameters") or [])
        except Exception:
            _MODEL_PARAMS["_unavailable"] = set()
    return param in _MODEL_PARAMS.get(model, set())


# ------------------------------ model listing ------------------------------

def list_openrouter_models(pattern=None, max_price_in=None):
    """Tool-capable OpenRouter models (id, context, $/M in, $/M out), from the
    public models endpoint — no key needed."""
    import urllib.request
    with urllib.request.urlopen(OPENROUTER_BASE + "/models", timeout=30) as r:
        data = json.load(r)["data"]
    rows = []
    rx = re.compile(pattern, re.I) if pattern else None
    for m in data:
        if "tools" not in (m.get("supported_parameters") or []):
            continue
        if rx and not rx.search(m["id"]):
            continue
        pr = m.get("pricing", {})
        pin = float(pr.get("prompt", 0)) * 1e6
        pout = float(pr.get("completion", 0)) * 1e6
        if max_price_in is not None and pin > max_price_in:
            continue
        rows.append((m["id"], m.get("context_length"), pin, pout,
                     "reasoning" in (m.get("supported_parameters") or [])))
    rows.sort(key=lambda r: (r[2], r[3]))
    return rows
