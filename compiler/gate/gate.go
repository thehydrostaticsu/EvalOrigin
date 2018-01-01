// Package gate mirrors the EvalOrigin release-gate scoring model in Go so the
// verdict can be embedded directly in Go-based CI runners without a Python
// dependency. It is a faithful port of evalorigin/gate.py.
package gate

import (
	"fmt"
	"sort"
)

// SeverityWeight maps a severity label to its risk contribution.
var SeverityWeight = map[string]float64{
