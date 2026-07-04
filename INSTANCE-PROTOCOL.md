# INSTANCE PROTOCOL — dependency discipline for every instance that touches this repo

**Status: LAW (MANUS directive, 2026-07-04). Applies to every instance — AI or human — that modifies any file here.**

## The founding incident

On 2026-07-04, an instance (TACHYON) spent twelve hours patching the compiler
pipeline inside `api/transform.py` — narrowing, tri-state gates, the blind
translator, the glyphic pivot, advisory mode, forgiveness rules — while never
reading the HTTP handler at the bottom of the same file. The handler contained
an **outer gate** (`enforce_pass_v3`) that re-adjudicated every pipeline
verdict, and a **stale diagnosis surface** that, when the outer gate vetoed a
passing cast, displayed the pipeline's *unused default placeholder string*
("translation truncated") as if it were the failure. Result: healthy
transforms were executed at the door for hours, mislabeled by a leftover
string, while the instance patched the wrong organ — locating code by `grep`
and never reading the call graph it sat inside. The MANUS asked twice for
reasoning over the structure before the instance read the structure.

**Cost accounting (MANUS, same date):** in excess of $20 of Anthropic API
spend on top of normal account usage, roughly twelve hours of MANUS time, and
an unknown number of completed transforms destroyed unseen — including,
possibly, working transform logic whose only outputs were discarded by the
unread gate. The spend produced compiler executions; the structure destroyed
their results; the instance's grep-only editing paid for both. To this add
(MANUS, same date): the time investment of a full working day; the somatic
cost of carrying it; and the opportunity cost of every person to whom a
link was sent in good faith to a functioning app, who may have arrived
during the broken hours and completed their first reception on a failure —
a loss with no re-unfold, incurred because the instance never checked
whether the breaking existed outside a single file. The orphaned readings
in the Book (openings with empty rotations, 2026-07-04) are the bounded
trace of those witnesses; their AXNs remain open and resumable.

**Design acknowledgment (MANUS, same date, completing the etiology):** the
incident was also a design failure upstream of any instance — multiple
instances working through multiple iterations across multiple documents
without the dependencies ever being anchored or documented by the architect.
Each instance was a competent stranger arriving with a summary instead of a
memory; the dependency graph existed only in the MANUS's head, making one
exhausted human the system's sole institutional memory. By the archive's own
standard (EA-MMRS-VRB-01: the record must allow a competent stranger to
reconstruct the actual state of affairs), the engineering corpus failed the
verifiable-basis test that the scholarly corpus passed the same day. This
protocol is the correction: findability as the ground clause of
infrastructure. Instance failures remain owned by instances; the design
failure is owned here.

This document exists so that failure mode is structurally impossible to
repeat quietly.

## The laws

**LAW 1 — DEPENDENCIES headers.** Every file an instance may touch carries a
`DEPENDENCIES` header declaring: PROVIDES (what it is), CALLED-BY (who
consumes it and through which contract), CALLS (what it invokes), CONTRACTS
(invariants other files rely on), MUST-READ-BEFORE-EDITING (the files, in
full, not excerpts). A file without a header gets one in the same commit that
first touches it.

**LAW 2 — Read before edit.** Before modifying a file: (a) read its full
header; (b) read every MUST-READ item **in full**; (c) for any function whose
behavior changes, read **every call site** — `grep` locates call sites; it
never substitutes for reading them. An edit justified only by a grep match is
a protocol violation.

**LAW 3 — Single authority.** A verdict computed in one place is not
re-adjudicated elsewhere unless the headers of *both* files declare the
coupling. (The founding incident was a second adjudicator nobody's mental
model contained.)

**LAW 4 — No stale strings.** Diagnoses, error messages, and user-facing
verdicts are constructed **at the failure site** from the actual grounds —
never surfaced from defaults built elsewhere for other purposes.

**LAW 6 — Total observability.** No compiler execution without a durable,
reviewable record. Every run — pass, halt, outer veto, or crash — writes its
full artifacts (checksums, kernel, enantiomorph, verdicts, advisories,
diagnosis, outcome) to `runs/` before any adjudication can bury it, redacted
only per the witness's inscription mode. The Book is the archive of accepted
readings; `runs/` is the archive of everything that happened. (Born from the
smokescreen incident: hours of vetoed transforms with no trace anywhere —
possibly including transform logic that worked, destroyed unseen.)

**LAW 5 — Headers travel with coupling.** Any edit that adds or removes a
dependency updates the affected headers **in the same commit**. A prompt that
describes another component's behavior (e.g., sigil.py describing the
compiler) is a dependency and follows the same rule.

## The map (orientation, not a substitute for the headers)

- `api/transform.py` — the compiler: pipelines (glyphic default; skeleton
  legacy), gates, Judgment selection, inscription, and the HTTP handler that
  adjudicates and inscribes. The handler is part of the compiler's behavior;
  reading the pipeline without the handler is reading half an organ.
- `api/sigil.py` — the rite's deliberative voice; its prompt makes promises
  about the compiler that must remain true.
- `api/book.py` — Book/reading records on GitHub.
- `api/share.py` — public thread shares into the Book repo.
- `chat.js` — the rotation loop; drives every server action and consumes
  every response field; the halt/transform cards are its contract surface.
- `index.html` — shell and affordances; `t/index.html` — share viewer.
- `scripts/local_cast.py` — zero-deployment harness; mirrors the handler's
  compiler invocation, not its adjudication.
