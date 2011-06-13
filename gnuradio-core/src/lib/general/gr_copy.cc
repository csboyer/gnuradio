/* -*- c++ -*- */
/*
 * Copyright 2006,2009 Free Software Foundation, Inc.
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gr_copy.h>
#include <gr_io_signature.h>
#include <string.h>

gr_copy_sptr
gr_make_copy(size_t itemsize)
{
  return gnuradio::get_initial_sptr(new gr_copy(itemsize));
}

gr_copy::gr_copy(size_t itemsize)
  : gr_block ("copy",
	      gr_make_io_signature2 (1, 2, itemsize, sizeof(char)),
	      gr_make_io_signature (1, 1, itemsize)),
    d_itemsize(itemsize),
    d_enabled(true)
{
}

bool
gr_copy::check_topology(int ninputs, int noutputs)
{
  return ninputs == noutputs || ninputs  == noutputs + 1;
}

int
gr_copy::general_work(int noutput_items,
		      gr_vector_int &ninput_items,
		      gr_vector_const_void_star &input_items,
		      gr_vector_void_star &output_items)
{
  const uint8_t *in = (const uint8_t *) input_items[0];
  uint8_t *out = (uint8_t *) output_items[0];
  int n, j;

  if(input_items.size() == 1) { //if only one input, do as original gr_copy

    n = std::min<int>(ninput_items[0], noutput_items);
    j = 0;

    if (d_enabled) {
      memcpy(out, in, n*d_itemsize);
      j = n;
    }
  }
  else {  //if two inputs, ignore enabled state, behave as new gr_copy
    const uint8_t *ctrl_sig = (const uint8_t *) input_items[1];
    j = 0;
    n = std::min<int>(ninput_items[0], ninput_items[1]);
    n = std::min<int>(n, noutput_items);
  
    for(int ii = 0; ii < n; ii++) {
      if(*ctrl_sig) {                 //check control signal, if not zero copy out
        memcpy(out, in, d_itemsize);  //copy to output
        out += d_itemsize;            //advance output pointer
        j++;
      }
      ctrl_sig++;                     //advance control signal pointer
      in += d_itemsize;               //advance input pointer
    }

  }

  consume_each(n);
  return j;
}
