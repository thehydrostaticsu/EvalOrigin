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
}

// Config holds the thresholds that drive the verdict.
type Config struct {
	BlockSeverities []string
	WarnThreshold   float64
	BlockThreshold  float64
}

// DefaultConfig returns the same defaults as the Python GateConfig.
func DefaultConfig() Config {
	return Config{
		BlockSeverities: []string{"critical"},
		WarnThreshold:   0.35,
		BlockThreshold:  0.65,
	}
}

// Summary is the gate verdict for a set of cases.
type Summary struct {
	Verdict       string         `json:"verdict"`
	Score         float64        `json:"score"`
	TotalCases    int            `json:"total_cases"`
	BlockingCases int            `json:"blocking_cases"`
	BySeverity    map[string]int `json:"by_severity"`
	Reasons       []string       `json:"reasons"`
}

func riskScore(cases []Case) float64 {
	if len(cases) == 0 {
		return 0.0
	}
	total := 0.0
	for _, c := range cases {
		w, ok := SeverityWeight[c.Severity]
		if !ok {
			w = 0.3
		}
		total += w
	}
	s := total / float64(len(cases))
	if s > 1.0 {
		s = 1.0
	}
	return s
}

func contains(list []string, target string) bool {
	for _, v := range list {
		if v == target {
			return true
		}
