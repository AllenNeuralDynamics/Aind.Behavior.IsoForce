using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Harp;
using AindIsoForceDataSchema.TaskLogic;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ThresholdJoystick
{

    private ForceThreshold threshold;
    public ForceThreshold Threshold
    {
        get { return threshold; }
        set { threshold = value; }
    }
    
    public IObservable<Timestamped<ThresholdedJoystickForce>> Process(IObservable<Timestamped<JoystickForce>> source)
    {
        return Process(source.Select(value => value.Value)).Zip(source, (force, timestamp) =>
        {
            return Timestamped.Create(force, timestamp.Seconds);
        });
    }


    public IObservable<ThresholdedJoystickForce> Process(IObservable<JoystickForce> source)
    {
        return source.Select(value =>
        {
            if (threshold == null)
            {
                throw new InvalidOperationException("Threshold property value is null.");
            }

            var left = threshold.Left.HasValue ? value.Left > threshold.Left.Value : false;
            var right = threshold.Right.HasValue ? value.Right > threshold.Right.Value : false;
            var push = threshold.Push.HasValue ? value.Push > threshold.Push.Value : false;
            var pull = threshold.Pull.HasValue ? value.Pull > threshold.Pull.Value : false;

            return new ThresholdedJoystickForce(){
                Left = left,
                Right = right,
                Push = push,
                Pull = pull
            };
        });
    }
}


public struct ThresholdedJoystickForce
{
    public bool Left;
    public bool Right;
    public bool Push;
    public bool Pull;

}
