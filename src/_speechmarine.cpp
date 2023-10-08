#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace nb = nanobind;

NB_MODULE(_speechmarine_impl, m) {
    m.def("gain_reduction_loop", [](
        nb::ndarray<double, nb::shape<nb::any>> gain_reduction,
        nb::ndarray<double, nb::shape<nb::any>> envelope,
        nb::ndarray<double, nb::shape<nb::any>> smoothed_envelope,
        double ratio,
        double threshold,
        double alpha_attack,
        double alpha_release)
    {
        double prev_envelope = smoothed_envelope(0);

        for(size_t i = 1; i < envelope.shape(0); i++) {
            double curr_envelope = envelope(i);
            double coeff = 0.0;
            if (curr_envelope > prev_envelope) {
                coeff = alpha_attack;
            } else {
                coeff = alpha_release;
            }
            // Optimize envelope storing:
            prev_envelope = coeff * prev_envelope + (1.0 - coeff) * curr_envelope;
            smoothed_envelope(i) = prev_envelope;
            // Calculate gain reduction
            if (prev_envelope > threshold) {
                double tmp = 1.0 / ratio;
                gain_reduction(i) = 1.0 - (1.0 - tmp) * (prev_envelope - threshold) / (prev_envelope - (threshold * tmp));
            }
            else {
                gain_reduction(i) = 1.0;
            }
        }

        return gain_reduction;  // ::ndarray<nb::numpy, const double, ... 
    });
}
