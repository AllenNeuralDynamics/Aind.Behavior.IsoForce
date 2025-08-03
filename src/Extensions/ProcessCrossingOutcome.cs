using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Harp;

namespace AindIsoForceDataSchema
{
    [Combinator]
    [Description("From two timestamped thresholded joystick forces, produces a crossing outcome with the action and duration.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class ProcessCrossingOutcome
    {
        public IObservable<CrossingOutcome> Process(IObservable<Tuple<Timestamped<ThresholdedJoystickForce>, Timestamped<ThresholdedJoystickForce>>> source)
        {
            return source.Select(value =>
            {
                var start = value.Item1;
                var end = value.Item2;

                return new CrossingOutcome()
                {
                    Start = new TimestampedThresholdedJoystickForce()
                    {
                        Value = start.Value,
                        Seconds = start.Seconds
                    },
                    End = new TimestampedThresholdedJoystickForce()
                    {
                        Value = end.Value,
                        Seconds = end.Seconds
                    },
                    Action = start.Value.TriggeredAction,
                    Duration = end.Seconds - start.Seconds
                };
            });
        }
    }
}
