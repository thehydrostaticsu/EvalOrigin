// Command evalgate reads a JSON array of compiled regression cases (or a full
// pack containing a "cases" array) on stdin or from a file, applies the
// EvalOrigin release-gate model, and prints the verdict as JSON.
//
// Exit codes: 0 = pass, 10 = warn, 20 = block, 2 = usage/parse error.
//
// Usage:
//
//	evalgate [--in cases.json] [--block-severities critical,high]
//	         [--warn 0.35] [--block 0.65]
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"
	"strings"

	"evalorigin/compiler/gate"
)

type packEnvelope struct {
	Cases []gate.Case `json:"cases"`
}

func readInput(path string) ([]byte, error) {
	if path == "" || path == "-" {
		return io.ReadAll(os.Stdin)
	}
	return os.ReadFile(path)
}

func parseCases(data []byte) ([]gate.Case, error) {
	trimmed := strings.TrimSpace(string(data))
	if trimmed == "" {
		return nil, fmt.Errorf("empty input")
	}
	if strings.HasPrefix(trimmed, "[") {
		var cases []gate.Case
		if err := json.Unmarshal(data, &cases); err != nil {
			return nil, err
		}
		return cases, nil
	}
