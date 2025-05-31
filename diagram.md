
```mermaid
    ---
    config:
    theme: mc
    look: classic
    ---
    classDiagram
        class QuiescencePeriod {
            +duration
            +threshold
        }
        class ResponsePeriod {
            +duration
            +attempt_threshold
            +time_threshold
        }
        class RewardPeriod {
            +duration
            +passive/active
        }
        class ITI {
            +duration
        }
        QuiescencePeriod --> ResponsePeriod : if force < threshold for duration
        ResponsePeriod --> ResponsePeriod : if force < attempt_threshold
        ResponsePeriod --> ITI : if force > attempt_threshold for < time_threshold
        ResponsePeriod --> RewardPeriod : if force > attempt_threshold for ≥ time_threshold
        RewardPeriod --> ITI : if lick then Reward
        ITI --> QuiescencePeriod : if wait > duration
```