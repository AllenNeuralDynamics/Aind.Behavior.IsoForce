using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using AindIsoForceDataSchema.TaskLogic;
using Bonsai.Harp;

[Combinator]
[Description("Parses a sequence of force values from a sequence of double arrays, applying the specified force operation settings.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ParseForce
{
    private ForceOperationControl forceOperationControl = new ForceOperationControl();
    public ForceOperationControl ForceOperationControl
    {
        get { return forceOperationControl; }
        set { forceOperationControl = value; }
    }

    public IObservable<Timestamped<JoystickForce>> Process(IObservable<Timestamped<double[]>> source)
    {
        return Process(source.Select(value => value.Value)).Zip(source, (force, timestamp) =>
        {
            return Timestamped.Create(force, timestamp.Seconds);
        });
    }

    public IObservable<JoystickForce> Process(IObservable<double[]> source)
    {
        return source.Select(value =>
        {
            var sett = forceOperationControl;
            if (sett == null)
            {
                throw new InvalidOperationException("ForceOperationControl property value is null.");
            }
            return new JoystickForce(value, sett);
        });
    }

}



[Description("Represents the force applied to a joystick, including left, right, push, and pull forces.")]
public class JoystickForce
{
    public JoystickForce(double[] value, ForceOperationControl sourceSettings)
    {
        if (sourceSettings == null)
        {
            throw new ArgumentNullException("sourceSettings input cannot be null.");
        }
        this.sourceSettings = sourceSettings;

        Left = (sourceSettings.Left.IsInverted ? 1.0 : -1.0) * value[sourceSettings.Left.Channel];
        Right = (sourceSettings.Right.IsInverted ? 1.0 : -1.0) * value[sourceSettings.Right.Channel];
        Push = (sourceSettings.Push.IsInverted ? 1.0 : -1.0) * value[sourceSettings.Push.Channel];
        Pull = (sourceSettings.Pull.IsInverted ? 1.0 : -1.0) * value[sourceSettings.Pull.Channel];
    }

    public double Left;
    public double Right;
    public double Push;
    public double Pull;
    public double RightLeft
    {
        get
        {
            if (sourceSettings.Left.Channel == sourceSettings.Right.Channel)
            {
                return Right;
            }
            else { return double.NaN; }
        }
    }
    public double PushPull
    {
        get
        {
            if (sourceSettings.Push.Channel == sourceSettings.Pull.Channel)
            {
                return Push;
            }
            else { return double.NaN; }
        }
    }

    public double this[AindIsoForceDataSchema.TaskLogic.Action index]
    {
        get
        {
            switch (index)
            {
                case AindIsoForceDataSchema.TaskLogic.Action.Left:
                    return Left;
                case AindIsoForceDataSchema.TaskLogic.Action.Right:
                    return Right;
                case AindIsoForceDataSchema.TaskLogic.Action.Push:
                    return Push;
                case AindIsoForceDataSchema.TaskLogic.Action.Pull:
                    return Pull;
                case AindIsoForceDataSchema.TaskLogic.Action.None:
                    return double.NaN;
                case AindIsoForceDataSchema.TaskLogic.Action.RightLeft:
                    return RightLeft;
                case AindIsoForceDataSchema.TaskLogic.Action.PushPull:
                    return PushPull;
                default:
                    throw new ArgumentOutOfRangeException("index", "Invalid action type specified.");
            }
        }
    }

    private ForceOperationControl sourceSettings;
    public ForceOperationControl SourceSettings
    {
        get { return sourceSettings; }
        private set { sourceSettings = value; }
    }
}
