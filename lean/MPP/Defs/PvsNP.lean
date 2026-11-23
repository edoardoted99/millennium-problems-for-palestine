import Mathlib

/-!
# P versus NP: definitions

**Draft. These definitions need review by complexity theorists before any
result stated with them can be taken to mean "P = NP" or "P ≠ NP".**

Languages are decision problems over binary strings, given by their
characteristic function `List Bool → Bool`. Machines are Mathlib's multi-stack
Turing machines (`Turing.FinTM2`); polynomial time is
`Turing.TM2ComputableInPolyTime`, measured in the length of the input.

* `InP L`: some machine decides `L` in polynomial time.
* `InNP L`: there is a polynomial-time verifier `V` and a polynomial `p` such
  that `L x` holds exactly when some witness `w` of length at most
  `p (length x)` makes `V` accept the pair `(x, w)`.
* `PEqualsNP`: every language in NP is in P.

Pairs are encoded by `pair`: each bit of `x` is doubled, then the separator
`[false, true]`, then `w` verbatim. The encoding is injective (gap `pnp-005`)
and computable in linear time.
-/

namespace MPP.PvsNP

open Computability Turing

/-- A language (decision problem) over binary strings. -/
abbrev Lang := List Bool → Bool

/-- `L` is decided by a multi-stack Turing machine in polynomial time. The input
string is written verbatim on the input stack; the answer is one symbol. -/
def InP (L : Lang) : Prop :=
  Nonempty (TM2ComputableInPolyTime (id : List Bool → List Bool) encodeBool L)

/-- Injective encoding of a pair of binary strings as one binary string. -/
def pair (x w : List Bool) : List Bool :=
  (x.flatMap fun b => [b, b]) ++ [false, true] ++ w

/-- `L` has polynomially bounded witnesses checkable in polynomial time. -/
def InNP (L : Lang) : Prop :=
  ∃ V : Lang, InP V ∧ ∃ p : Polynomial ℕ, ∀ x : List Bool,
    (L x = true ↔ ∃ w : List Bool, w.length ≤ p.eval x.length ∧ V (pair x w) = true)

/-- Every language in NP is in P. -/
def PEqualsNP : Prop :=
  ∀ L : Lang, InNP L → InP L

end MPP.PvsNP
