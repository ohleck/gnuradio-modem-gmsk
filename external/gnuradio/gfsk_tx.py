#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK TX
# Generated: Sun Apr 28 18:49:34 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
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
import math
import sip
import sys
from gnuradio import qtgui


class gfsk_tx(gr.top_block, Qt.QWidget):

    def __init__(self, baudrate=9600, default_attenuation=10, default_dev=4950/2, default_input=0, default_ip='127.0.0.1', default_port=5000, freq=435750000, samp_rate_tx=1920000, sdr_dev='uhd=0'):
        gr.top_block.__init__(self, "GFSK TX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GFSK TX")
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

        self.settings = Qt.QSettings("GNU Radio", "gfsk_tx")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Parameters
        ##################################################
        self.baudrate = baudrate
        self.default_attenuation = default_attenuation
        self.default_dev = default_dev
        self.default_input = default_input
        self.default_ip = default_ip
        self.default_port = default_port
        self.freq = freq
        self.samp_rate_tx = samp_rate_tx
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.interp_tx = interp_tx = samp_rate_tx/baudrate
        self.sensitivity = sensitivity = 2*math.pi*default_dev/samp_rate_tx

        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1, samp_rate_tx, interp_tx, 0.3, 88)

        self.freq_offset = freq_offset = 1700
        self.bt = bt = 0.5
        self.attenuation = attenuation = default_attenuation

        ##################################################
        # Blocks
        ##################################################
        self._freq_offset_range = Range(-20000, 20000, 100, 1700, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Signal Frequency Offset', "counter_slider", int)
        self.top_grid_layout.addWidget(self._freq_offset_win, 0, 2, 1, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(2,4)]
        self._bt_range = Range(0, 1, 0.05, 0.5, 200)
        self._bt_win = RangeWidget(self._bt_range, self.set_bt, 'Gaussian BT', "counter_slider", float)
        self.top_grid_layout.addWidget(self._bt_win, 0, 4, 1, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(4,6)]
        self._attenuation_range = Range(0, 100, 1, default_attenuation, 200)
        self._attenuation_win = RangeWidget(self._attenuation_range, self.set_attenuation, 'Signal Attenuation', "counter_slider", int)
        self.top_grid_layout.addWidget(self._attenuation_win, 0, 0, 1, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,2)]
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_tx, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 0, 2, 6)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(3,5)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	500, #size
        	samp_rate_tx, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

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
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,3)]
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate_tx, #bw
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

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
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 3, 1, 3)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(3,6)]
        self.iio_fmcomms2_sink_0 = iio.fmcomms2_sink_f32c('ip:pluto.local', freq+freq_offset, samp_rate_tx, 1 - 1, 20000000, True, False, 0x8000, False, "A", attenuation, 10.0, '', True)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=interp_tx,
        	sensitivity=sensitivity,
        	bt=bt,
        	verbose=False,
        	log=False,
        )
        self.blks2_tcp_source = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_char*1,
        	addr=default_ip,
        	port=default_port,
        	server=True,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_tcp_source, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.iio_fmcomms2_sink_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gfsk_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.set_interp_tx(self.samp_rate_tx/self.baudrate)

    def get_default_attenuation(self):
        return self.default_attenuation

    def set_default_attenuation(self, default_attenuation):
        self.default_attenuation = default_attenuation
        self.set_attenuation(self.default_attenuation)

    def get_default_dev(self):
        return self.default_dev

    def set_default_dev(self, default_dev):
        self.default_dev = default_dev
        self.set_sensitivity(2*math.pi*self.default_dev/self.samp_rate_tx)

    def get_default_input(self):
        return self.default_input

    def set_default_input(self, default_input):
        self.default_input = default_input

    def get_default_ip(self):
        return self.default_ip

    def set_default_ip(self, default_ip):
        self.default_ip = default_ip

    def get_default_port(self):
        return self.default_port

    def set_default_port(self, default_port):
        self.default_port = default_port

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_fmcomms2_sink_0.set_params(self.freq+self.freq_offset, self.samp_rate_tx, 20000000, "A", self.attenuation, 10.0, '', True)

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.set_sensitivity(2*math.pi*self.default_dev/self.samp_rate_tx)
        self.set_interp_tx(self.samp_rate_tx/self.baudrate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate_tx)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate_tx)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate_tx)
        self.iio_fmcomms2_sink_0.set_params(self.freq+self.freq_offset, self.samp_rate_tx, 20000000, "A", self.attenuation, 10.0, '', True)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_interp_tx(self):
        return self.interp_tx

    def set_interp_tx(self, interp_tx):
        self.interp_tx = interp_tx

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.iio_fmcomms2_sink_0.set_params(self.freq+self.freq_offset, self.samp_rate_tx, 20000000, "A", self.attenuation, 10.0, '', True)

    def get_bt(self):
        return self.bt

    def set_bt(self, bt):
        self.bt = bt

    def get_attenuation(self):
        return self.attenuation

    def set_attenuation(self, attenuation):
        self.attenuation = attenuation
        self.iio_fmcomms2_sink_0.set_params(self.freq+self.freq_offset, self.samp_rate_tx, 20000000, "A", self.attenuation, 10.0, '', True)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-b", "--baudrate", dest="baudrate", type="intx", default=9600,
        help="Set baudrate [default=%default]")
    parser.add_option(
        "-g", "--default-attenuation", dest="default_attenuation", type="intx", default=10,
        help="Set Input [default=%default]")
    parser.add_option(
        "-j", "--default-dev", dest="default_dev", type="intx", default=4950/2,
        help="Set Input [default=%default]")
    parser.add_option(
        "-q", "--default-input", dest="default_input", type="intx", default=0,
        help="Set Input [default=%default]")
    parser.add_option(
        "-i", "--default-ip", dest="default_ip", type="string", default='127.0.0.1',
        help="Set default_ip [default=%default]")
    parser.add_option(
        "-p", "--default-port", dest="default_port", type="intx", default=5000,
        help="Set default_port [default=%default]")
    parser.add_option(
        "-f", "--freq", dest="freq", type="intx", default=435750000,
        help="Set frequency [default=%default]")
    parser.add_option(
        "-s", "--samp-rate-tx", dest="samp_rate_tx", type="intx", default=1920000,
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "-d", "--sdr-dev", dest="sdr_dev", type="string", default='uhd=0',
        help="Set SDR Device [default=%default]")
    return parser


def main(top_block_cls=gfsk_tx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(baudrate=options.baudrate, default_attenuation=options.default_attenuation, default_dev=options.default_dev, default_input=options.default_input, default_ip=options.default_ip, default_port=options.default_port, freq=options.freq, samp_rate_tx=options.samp_rate_tx, sdr_dev=options.sdr_dev)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
