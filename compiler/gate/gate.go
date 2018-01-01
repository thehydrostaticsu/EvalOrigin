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
	"critical": 1.0,
	"high":     0.7,
	"medium":   0.4,
	"low":      0.2,
	"info":     0.05,
}

// Case is the minimal shape of a compiled regression case needed to gate.
type Case struct {
	CaseID     string `json:"case_id"`
	Entrypoint string `json:"entrypoint"`
	Severity   string `json:"severity"`
	Steps      int    `json:"steps"`
