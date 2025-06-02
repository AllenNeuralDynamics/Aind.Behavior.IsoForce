using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Harp;

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
            if (start.Value[start.Value.TriggeredAction] == end.Value[start.Value.TriggeredAction])
            {
                throw new InvalidOperationException("Start and end actions must be different.");
            }
            return new CrossingOutcome()
            {
                Start = start,
                End = end,
                Action = start.Value.TriggeredAction,
                Duration = end.Seconds - start.Seconds
            };
        });
    }
}


public class CrossingOutcome
{
    public AindIsoForceDataSchema.TaskLogic.Action Action { get; set; }
    public double Duration  { get; set; }
    public Timestamped<ThresholdedJoystickForce> Start  { get; set; }
    public Timestamped<ThresholdedJoystickForce> End  { get; set;}
}
