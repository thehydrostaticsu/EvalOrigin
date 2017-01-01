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
