using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Harp;


namespace AindIsoForceDataSchema
{
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
}
