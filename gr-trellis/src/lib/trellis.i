/* -*- c++ -*- */
/*
 * Copyright 2009 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

%include "gnuradio.i"			// the common stuff

%{
#include "fsm.h"
#include "interleaver.h"
#include "trellis_permutation.h"
#include "trellis_siso_f.h"
#include "trellis_siso_combined_f.h"
%}

// ----------------------------------------------------------------

%include "fsm.i"
%include "interleaver.i"
%include "trellis_permutation.i"
%include "trellis_siso_f.i"
%include "trellis_siso_combined_f.i"

%include "metric_type.h"
%include "siso_type.h"


%include "trellis_generated.i"

#if SWIGGUILE
%scheme %{
(load-extension-global "libguile-gnuradio-trellis" "scm_init_gnuradio_trellis_module")
%}

%goops %{
(use-modules (gnuradio gnuradio_core_runtime))
%}
#endif
