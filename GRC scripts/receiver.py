#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Receiver
# Generated: Sun Jan 31 19:56:32 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx

class receiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.olin_uhd09 = uhd.usrp_source(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.olin_uhd09.set_samp_rate(samp_rate)
        self.olin_uhd09.set_center_freq(2.4855e9, 0)
        self.olin_uhd09.set_gain(200, 0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "test.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, samp_rate, 400, 600, 100, firdes.WIN_HAMMING, 6.76))
        self.analog_pll_freqdet_cf_0 = analog.pll_freqdet_cf(3.14/100, 3.14, 3.14)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.olin_uhd09, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_pll_freqdet_cf_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_pll_freqdet_cf_0, 0), (self.wxgui_scopesink2_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.olin_uhd09.set_samp_rate(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 400, 600, 100, firdes.WIN_HAMMING, 6.76))
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = receiver()
    tb.Start(True)
    tb.Wait()

