#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GMSK Receiver (GFSK based)
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import correctiq
import math
import satellites
import sip
import sys
from gnuradio import qtgui


class gmsk_rx_v1(gr.top_block, Qt.QWidget):

    def __init__(self, default_bandwidth=20e3, default_baud=9600, default_bin_file_sink="/tmp/rx_data.bin", default_dev=4950/2, default_freq=435750000, default_gain=16, default_ip='127.0.0.1', default_port=7000, default_samp=1920000, sdr_dev="rtl=0"):
        gr.top_block.__init__(self, "GMSK Receiver (GFSK based)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GMSK Receiver (GFSK based)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "gmsk_rx_v1")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.default_bandwidth = default_bandwidth
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_dev = default_dev
        self.default_freq = default_freq
        self.default_gain = default_gain
        self.default_ip = default_ip
        self.default_port = default_port
        self.default_samp = default_samp
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_dec = samp_rate_dec = default_baud*8
        self.interp_tx = interp_tx = default_samp/default_baud
        self.dec_rx = dec_rx = default_samp/samp_rate_dec
        self.sps_rx = sps_rx = interp_tx/dec_rx
        self.t_points = t_points = 5000
        self.rx_gain = rx_gain = 64

        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1, samp_rate_dec, sps_rx, 0.3, 88)


        self.low_pass_taps_2 = low_pass_taps_2 = firdes.low_pass(1.0, samp_rate_dec, 9600, 1200, firdes.WIN_HAMMING, 6.76)


        self.low_pass_taps = low_pass_taps = firdes.low_pass(1.0, default_samp, 150000, 20000, firdes.WIN_HAMMING, 6.76)

        self.freq_xlating = freq_xlating = 000000
        self.freq_offset = freq_offset = 2200
        self.filter_offset = filter_offset = 0
        self.demod_gain = demod_gain = (samp_rate_dec)/(2*math.pi*default_dev)
        self.cc_omega_lim = cc_omega_lim = 0.002
        self.cc_mu_gain = cc_mu_gain = 0.175
        self.cc_mu = cc_mu = 0.5
        self.cc_gain = cc_gain = 0.25*0.175*0.175

        ##################################################
        # Blocks
        ##################################################
        self.controls = Qt.QTabWidget()
        self.controls_widget_0 = Qt.QWidget()
        self.controls_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_0)
        self.controls_grid_layout_0 = Qt.QGridLayout()
        self.controls_layout_0.addLayout(self.controls_grid_layout_0)
        self.controls.addTab(self.controls_widget_0, 'RF')
        self.controls_widget_1 = Qt.QWidget()
        self.controls_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_1)
        self.controls_grid_layout_1 = Qt.QGridLayout()
        self.controls_layout_1.addLayout(self.controls_grid_layout_1)
        self.controls.addTab(self.controls_widget_1, 'Filter/Demod')
        self.controls_widget_2 = Qt.QWidget()
        self.controls_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_2)
        self.controls_grid_layout_2 = Qt.QGridLayout()
        self.controls_layout_2.addLayout(self.controls_grid_layout_2)
        self.controls.addTab(self.controls_widget_2, 'Receiver DSP')
        self.top_grid_layout.addWidget(self.controls, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._demod_gain_range = Range(1, 100, 1, (samp_rate_dec)/(2*math.pi*default_dev), 200)
        self._demod_gain_win = RangeWidget(self._demod_gain_range, self.set_demod_gain, 'Demodulator Gain', "counter_slider", float)
        self.controls_grid_layout_1.addWidget(self._demod_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_1.setColumnStretch(c, 1)
        self.signals = Qt.QTabWidget()
        self.signals_widget_0 = Qt.QWidget()
        self.signals_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_0)
        self.signals_grid_layout_0 = Qt.QGridLayout()
        self.signals_layout_0.addLayout(self.signals_grid_layout_0)
        self.signals.addTab(self.signals_widget_0, 'Receiver')
        self.signals_widget_1 = Qt.QWidget()
        self.signals_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_1)
        self.signals_grid_layout_1 = Qt.QGridLayout()
        self.signals_layout_1.addLayout(self.signals_grid_layout_1)
        self.signals.addTab(self.signals_widget_1, 'Filter RX')
        self.signals_widget_2 = Qt.QWidget()
        self.signals_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_2)
        self.signals_grid_layout_2 = Qt.QGridLayout()
        self.signals_layout_2.addLayout(self.signals_grid_layout_2)
        self.signals.addTab(self.signals_widget_2, 'Modulator')
        self.signals_widget_3 = Qt.QWidget()
        self.signals_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_3)
        self.signals_grid_layout_3 = Qt.QGridLayout()
        self.signals_layout_3.addLayout(self.signals_grid_layout_3)
        self.signals.addTab(self.signals_widget_3, 'Dec Filter')
        self.signals_widget_4 = Qt.QWidget()
        self.signals_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_4)
        self.signals_grid_layout_4 = Qt.QGridLayout()
        self.signals_layout_4.addLayout(self.signals_grid_layout_4)
        self.signals.addTab(self.signals_widget_4, 'Clock Recovery/Bitstream')
        self.top_grid_layout.addWidget(self.signals, 1, 0, 2, 4)
        for r in range(1, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = Range(0, 100, 1, 64, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Power Gain', "counter_slider", float)
        self.controls_grid_layout_0.addWidget(self._rx_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-20000, 20000, 100, 2200, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Signal Frequency Offset', "counter_slider", int)
        self.controls_grid_layout_0.addWidget(self._freq_offset_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self._filter_offset_range = Range(-1*demod_gain, 1*demod_gain, 0.01, 0, 200)
        self._filter_offset_win = RangeWidget(self._filter_offset_range, self.set_filter_offset, 'Signal Offset', "counter_slider", float)
        self.controls_grid_layout_1.addWidget(self._filter_offset_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.controls_grid_layout_1.setColumnStretch(c, 1)
        self._cc_omega_lim_range = Range(0.0005, 0.02, 0.0001, 0.002, 200)
        self._cc_omega_lim_win = RangeWidget(self._cc_omega_lim_range, self.set_cc_omega_lim, 'CC Omega Lim', "counter_slider", float)
        self.controls_grid_layout_2.addWidget(self._cc_omega_lim_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_2.setRowStretch(r, 1)
        for c in range(3, 4):
            self.controls_grid_layout_2.setColumnStretch(c, 1)
        self._cc_mu_gain_range = Range(0.01, 0.5, 0.05, 0.175, 200)
        self._cc_mu_gain_win = RangeWidget(self._cc_mu_gain_range, self.set_cc_mu_gain, 'CC MU gain', "counter_slider", float)
        self.controls_grid_layout_2.addWidget(self._cc_mu_gain_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.controls_grid_layout_2.setColumnStretch(c, 1)
        self._cc_mu_range = Range(0.1, 2, 0.1, 0.5, 200)
        self._cc_mu_win = RangeWidget(self._cc_mu_range, self.set_cc_mu, 'CC MU', "counter_slider", float)
        self.controls_grid_layout_2.addWidget(self._cc_mu_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.controls_grid_layout_2.setColumnStretch(c, 1)
        self.satellites_nrzi_decode_0_0 = satellites.nrzi_decode()
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.qtgui_waterfall_sink_x_0_0_0_0_0 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_0_win, 1, 3, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_3.setRowStretch(r, 1)
        for c in range(3, 6):
            self.signals_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0_0 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win, 1, 3, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_2.setRowStretch(r, 1)
        for c in range(3, 6):
            self.signals_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 1, 3, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_1.setRowStretch(r, 1)
        for c in range(3, 6):
            self.signals_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.0000010)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 2, 0, 1, 6)
        for r in range(2, 3):
            self.signals_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 6):
            self.signals_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0_1 = qtgui.time_sink_f(
        	t_points, #size
        	samp_rate_dec, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_1.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_1_win, 0, 0, 1, 6)
        for r in range(0, 1):
            self.signals_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 6):
            self.signals_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0 = qtgui.time_sink_f(
        	t_points, #size
        	samp_rate_dec/8, #samp_rate
        	'Time RX In', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0_0_0.disable_legend()

        labels = ['Clock Recovery', 'Bitstream', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, 0, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_4.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_0_0_win, 0, 0, 2, 2)
        for r in range(0, 2):
            self.signals_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 2):
            self.signals_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0_0 = qtgui.time_sink_f(
        	t_points*2, #size
        	samp_rate_dec, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_win, 0, 0, 1, 6)
        for r in range(0, 1):
            self.signals_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 6):
            self.signals_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_c(
        	200, #size
        	samp_rate_dec, #samp_rate
        	'Time RX In', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 0, 0, 1, 6)
        for r in range(0, 1):
            self.signals_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 6):
            self.signals_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_c(
        	t_points+1000, #size
        	default_samp, #samp_rate
        	'Time RX In', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_win, 0, 0, 1, 3)
        for r in range(0, 1):
            self.signals_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 3):
            self.signals_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_0_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 3):
            self.signals_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 3):
            self.signals_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_dec, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_1_0_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.signals_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 3):
            self.signals_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1 = qtgui.freq_sink_c(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1.set_update_time(0.0000010)
        self.qtgui_freq_sink_x_0_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_1_win, 0, 3, 1, 3)
        for r in range(0, 1):
            self.signals_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 6):
            self.signals_grid_layout_0.setColumnStretch(c, 1)
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source_f32c('ip:pluto.local', default_freq-freq_xlating+freq_offset, default_samp, 20000000, True, False, 0x8000, True, True, True, "fast_attack", rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(dec_rx, (low_pass_taps), freq_xlating, default_samp)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(1, (low_pass_taps_2))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sps_rx, 0.25*0.175*0.175, cc_mu, cc_mu_gain, cc_omega_lim)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.correctiq_correctiq_0 = correctiq.correctiq()
        self._cc_gain_range = Range(1e-3, 50e-3, 1e-3, 0.25*0.175*0.175, 200)
        self._cc_gain_win = RangeWidget(self._cc_gain_range, self.set_cc_gain, 'CC Omega Gain', "counter_slider", float)
        self.controls_grid_layout_2.addWidget(self._cc_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_2.setColumnStretch(c, 1)
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((filter_offset*demod_gain, ))
        self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
        	itemsize=gr.sizeof_char*1,
        	addr=default_ip,
        	port=default_port,
        	server=True,
        )
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(demod_gain)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_0_0, 1))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blks2_tcp_sink_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0_1_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.correctiq_correctiq_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_freq_sink_x_0_0_1, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.satellites_nrzi_decode_0_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gmsk_rx_v1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_default_bandwidth(self):
        return self.default_bandwidth

    def set_default_bandwidth(self, default_bandwidth):
        self.default_bandwidth = default_bandwidth

    def get_default_baud(self):
        return self.default_baud

    def set_default_baud(self, default_baud):
        self.default_baud = default_baud
        self.set_samp_rate_dec(self.default_baud*8)
        self.set_interp_tx(self.default_samp/self.default_baud)

    def get_default_bin_file_sink(self):
        return self.default_bin_file_sink

    def set_default_bin_file_sink(self, default_bin_file_sink):
        self.default_bin_file_sink = default_bin_file_sink

    def get_default_dev(self):
        return self.default_dev

    def set_default_dev(self, default_dev):
        self.default_dev = default_dev
        self.set_demod_gain((self.samp_rate_dec)/(2*math.pi*self.default_dev))

    def get_default_freq(self):
        return self.default_freq

    def set_default_freq(self, default_freq):
        self.default_freq = default_freq
        self.iio_fmcomms2_source_0.set_params(self.default_freq-self.freq_xlating+self.freq_offset, self.default_samp, 20000000, True, True, True, "fast_attack", self.rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)

    def get_default_gain(self):
        return self.default_gain

    def set_default_gain(self, default_gain):
        self.default_gain = default_gain

    def get_default_ip(self):
        return self.default_ip

    def set_default_ip(self, default_ip):
        self.default_ip = default_ip

    def get_default_port(self):
        return self.default_port

    def set_default_port(self, default_port):
        self.default_port = default_port

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.set_dec_rx(self.default_samp/self.samp_rate_dec)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.default_samp)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.default_samp)
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(0, self.default_samp)
        self.set_interp_tx(self.default_samp/self.default_baud)
        self.iio_fmcomms2_source_0.set_params(self.default_freq-self.freq_xlating+self.freq_offset, self.default_samp, 20000000, True, True, True, "fast_attack", self.rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_samp_rate_dec(self):
        return self.samp_rate_dec

    def set_samp_rate_dec(self, samp_rate_dec):
        self.samp_rate_dec = samp_rate_dec
        self.set_demod_gain((self.samp_rate_dec)/(2*math.pi*self.default_dev))
        self.set_dec_rx(self.default_samp/self.samp_rate_dec)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(0, self.samp_rate_dec)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(0, self.samp_rate_dec)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(0, self.samp_rate_dec)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_samp_rate(self.samp_rate_dec)
        self.qtgui_time_sink_x_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate_dec/8)
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.samp_rate_dec)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate_dec)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_frequency_range(0, self.samp_rate_dec)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(0, self.samp_rate_dec)
        self.qtgui_freq_sink_x_0_0_1_0.set_frequency_range(0, self.samp_rate_dec)

    def get_interp_tx(self):
        return self.interp_tx

    def set_interp_tx(self, interp_tx):
        self.interp_tx = interp_tx
        self.set_sps_rx(self.interp_tx/self.dec_rx)

    def get_dec_rx(self):
        return self.dec_rx

    def set_dec_rx(self, dec_rx):
        self.dec_rx = dec_rx
        self.set_sps_rx(self.interp_tx/self.dec_rx)

    def get_sps_rx(self):
        return self.sps_rx

    def set_sps_rx(self, sps_rx):
        self.sps_rx = sps_rx
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sps_rx)

    def get_t_points(self):
        return self.t_points

    def set_t_points(self, t_points):
        self.t_points = t_points

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.iio_fmcomms2_source_0.set_params(self.default_freq-self.freq_xlating+self.freq_offset, self.default_samp, 20000000, True, True, True, "fast_attack", self.rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_low_pass_taps_2(self):
        return self.low_pass_taps_2

    def set_low_pass_taps_2(self, low_pass_taps_2):
        self.low_pass_taps_2 = low_pass_taps_2
        self.fir_filter_xxx_0_0.set_taps((self.low_pass_taps_2))

    def get_low_pass_taps(self):
        return self.low_pass_taps

    def set_low_pass_taps(self, low_pass_taps):
        self.low_pass_taps = low_pass_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.low_pass_taps))

    def get_freq_xlating(self):
        return self.freq_xlating

    def set_freq_xlating(self, freq_xlating):
        self.freq_xlating = freq_xlating
        self.iio_fmcomms2_source_0.set_params(self.default_freq-self.freq_xlating+self.freq_offset, self.default_samp, 20000000, True, True, True, "fast_attack", self.rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq_xlating)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.iio_fmcomms2_source_0.set_params(self.default_freq-self.freq_xlating+self.freq_offset, self.default_samp, 20000000, True, True, True, "fast_attack", self.rx_gain, "fast_attack", 64.0, "A_BALANCED", '', True)

    def get_filter_offset(self):
        return self.filter_offset

    def set_filter_offset(self, filter_offset):
        self.filter_offset = filter_offset
        self.blocks_add_const_vxx_0.set_k((self.filter_offset*self.demod_gain, ))

    def get_demod_gain(self):
        return self.demod_gain

    def set_demod_gain(self, demod_gain):
        self.demod_gain = demod_gain
        self.blocks_add_const_vxx_0.set_k((self.filter_offset*self.demod_gain, ))
        self.analog_quadrature_demod_cf_0.set_gain(self.demod_gain)

    def get_cc_omega_lim(self):
        return self.cc_omega_lim

    def set_cc_omega_lim(self, cc_omega_lim):
        self.cc_omega_lim = cc_omega_lim

    def get_cc_mu_gain(self):
        return self.cc_mu_gain

    def set_cc_mu_gain(self, cc_mu_gain):
        self.cc_mu_gain = cc_mu_gain
        self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.cc_mu_gain)

    def get_cc_mu(self):
        return self.cc_mu

    def set_cc_mu(self, cc_mu):
        self.cc_mu = cc_mu
        self.digital_clock_recovery_mm_xx_0.set_mu(self.cc_mu)

    def get_cc_gain(self):
        return self.cc_gain

    def set_cc_gain(self, cc_gain):
        self.cc_gain = cc_gain


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-w", "--default-bandwidth", dest="default_bandwidth", type="eng_float", default=eng_notation.num_to_str(20e3),
        help="Set default_bandwidth [default=%default]")
    parser.add_option(
        "-b", "--default-baud", dest="default_baud", type="intx", default=9600,
        help="Set default_baud [default=%default]")
    parser.add_option(
        "-o", "--default-bin-file-sink", dest="default_bin_file_sink", type="string", default="/tmp/rx_data.bin",
        help="Set default_bin_file_sink [default=%default]")
    parser.add_option(
        "-j", "--default-dev", dest="default_dev", type="eng_float", default=eng_notation.num_to_str(4950/2),
        help="Set Input [default=%default]")
    parser.add_option(
        "-f", "--default-freq", dest="default_freq", type="intx", default=435750000,
        help="Set default_freq [default=%default]")
    parser.add_option(
        "-g", "--default-gain", dest="default_gain", type="eng_float", default=eng_notation.num_to_str(16),
        help="Set default_gain [default=%default]")
    parser.add_option(
        "-i", "--default-ip", dest="default_ip", type="string", default='127.0.0.1',
        help="Set default_ip [default=%default]")
    parser.add_option(
        "-p", "--default-port", dest="default_port", type="intx", default=7000,
        help="Set default_port [default=%default]")
    parser.add_option(
        "-s", "--default-samp", dest="default_samp", type="intx", default=1920000,
        help="Set default_samp [default=%default]")
    parser.add_option(
        "-d", "--sdr-dev", dest="sdr_dev", type="string", default="rtl=0",
        help="Set sdr_dev [default=%default]")
    return parser


def main(top_block_cls=gmsk_rx_v1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(default_bandwidth=options.default_bandwidth, default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_dev=options.default_dev, default_freq=options.default_freq, default_gain=options.default_gain, default_ip=options.default_ip, default_port=options.default_port, default_samp=options.default_samp, sdr_dev=options.sdr_dev)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
