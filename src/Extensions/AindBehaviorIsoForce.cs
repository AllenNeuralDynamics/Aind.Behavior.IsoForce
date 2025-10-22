using System;

namespace AindIsoForceDataSchema
{
    public partial class JoystickForce
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
            RightLeft = (sourceSettings.Left.Channel == sourceSettings.Right.Channel) ? Right : double.NaN;
            PushPull = (sourceSettings.Push.Channel == sourceSettings.Pull.Channel) ? Push : double.NaN;
        }


        public double this[AindIsoForceDataSchema.Action index]
        {
            get
            {
                switch (index)
                {
                    case Action.Left:
                        return Left;
                    case Action.Right:
                        return Right;
                    case Action.Push:
                        return Push;
                    case Action.Pull:
                        return Pull;
                    case Action.None:
                        return double.NaN;
                    case Action.RightLeft:
                        return RightLeft;
                    case Action.PushPull:
                        return PushPull;
                    default:
                        throw new ArgumentOutOfRangeException("index", "Invalid action type specified.");
                }
            }
        }

        [System.Xml.Serialization.XmlIgnore]
        private ForceOperationControl sourceSettings;
        public ForceOperationControl SourceSettings
        {
            get { return sourceSettings; }
            private set { sourceSettings = value; }
        }
    }


    public partial class ThresholdedJoystickForce
    {

        [System.Xml.Serialization.XmlIgnore]
        public bool IsAny
        {
            get
            {
                return Left || Right || Push || Pull;
            }
        }

        public bool this[Action index]
        {
            get
            {
                switch (index)
                {
                    case Action.Left:
                        return Left;
                    case Action.Right:
                        return Right;
                    case Action.Push:
                        return Push;
                    case Action.Pull:
                        return Pull;
                    case Action.None:
                        return false;
                    case Action.RightLeft:
                        return Left || Right;
                    case Action.PushPull:
                        return Push || Pull;
                    default:
                        return false;
                }
            }
        }

        public Action TriggeredAction
        {
            get
            {
                if (Left)
                {
                    return Action.Left;
                }
                else if (Right)
                {
                    return Action.Right;
                }
                else if (Push)
                {
                    return Action.Push;
                }
                else if (Pull)
                {
                    return Action.Pull;
                }
                else
                {
                    return Action.None;
                }
            }
        }

    }
}
