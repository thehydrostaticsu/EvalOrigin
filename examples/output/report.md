# EvalOrigin Report - `pack-8ede0409f83f`

**Gate verdict:** BLOCK

- Risk score: `0.61`
- Total cases: `7`
- Blocking cases: `1`
- Entrypoints: `auth.verify`, `checkout.total`, `etl.transform`, `report.render`, `search.query`

## Gate reasons

- 1 case(s) at blocking severity ['critical']

## Severity distribution

| Severity | Cases |
| --- | --- |
| critical | 1 |
| high | 3 |
| medium | 3 |

## Regression cases

| Case | Entrypoint | Severity | Origin | Given | Expect |
| --- | --- | --- | --- | --- | --- |
| case-830a112dd507 | checkout.total | critical | incident:INC-2041 | {'cart_id': 'c-88'} | {'total': 4207, 'currency': 'USD'} |
| case-1af79f6e3803 | auth.verify | high | incident:INC-1990 | {'token': 'eyJ...redacted'} | {'valid': False, 'reason': 'expired'} |
| case-950e718d20af | etl.transform | high | trace-failure | {'path': 's3://raw/day.csv'} | {'rows': 100} |
| case-4dde576108e3 | report.render | high | trace-failure | {'window': '24h'} | {'bytes': 20480} |
| case-bdaeb8c13845 | etl.transform | medium | golden-path | {'path': 's3://raw/day.csv'} | {'rows': 100} |
| case-de5cb01f3874 | report.render | medium | golden-path | {'window': '24h'} | {'bytes': 20480} |
| case-be38b325e33b | search.query | medium | incident:INC-1877 | {'alias': 'products'} | {'hits': 12, 'generation': 8} |

## Rubrics

### `auth.verify` - rubric-cc972827df26

| Criterion | Weight | Check | Description |
| --- | --- | --- | --- |
| output_matches | 0.38 | equals(expect) | Candidate output equals the pinned expectation. |
| no_error_status | 0.25 | all_steps_ok | No step reports an error or failed status. |
| within_step_budget | 0.12 | steps<=2 | Execution completes within 2 recorded steps. |
| severity_guard | 0.25 | no_waiver_on_high | High/critical origin cases must pass without waivers. |

### `checkout.total` - rubric-cd6eb721dffa

| Criterion | Weight | Check | Description |
| --- | --- | --- | --- |
| output_matches | 0.38 | equals(expect) | Candidate output equals the pinned expectation. |
| no_error_status | 0.25 | all_steps_ok | No step reports an error or failed status. |
| within_step_budget | 0.12 | steps<=3 | Execution completes within 3 recorded steps. |
| severity_guard | 0.25 | no_waiver_on_high | High/critical origin cases must pass without waivers. |

### `etl.transform` - rubric-d261bc7fb729

| Criterion | Weight | Check | Description |
| --- | --- | --- | --- |
| output_matches | 0.38 | equals(expect) | Candidate output equals the pinned expectation. |
| no_error_status | 0.25 | all_steps_ok | No step reports an error or failed status. |
| within_step_budget | 0.12 | steps<=2 | Execution completes within 2 recorded steps. |
| severity_guard | 0.25 | no_waiver_on_high | High/critical origin cases must pass without waivers. |

### `report.render` - rubric-03db80a5a36a

| Criterion | Weight | Check | Description |
| --- | --- | --- | --- |
| output_matches | 0.38 | equals(expect) | Candidate output equals the pinned expectation. |
| no_error_status | 0.25 | all_steps_ok | No step reports an error or failed status. |
| within_step_budget | 0.12 | steps<=2 | Execution completes within 2 recorded steps. |
| severity_guard | 0.25 | no_waiver_on_high | High/critical origin cases must pass without waivers. |

### `search.query` - rubric-f3c9ec0cb4ae

| Criterion | Weight | Check | Description |
| --- | --- | --- | --- |
