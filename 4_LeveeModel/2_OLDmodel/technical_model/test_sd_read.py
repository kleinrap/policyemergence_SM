 # pylab inline
import pysd
model = pysd.read_vensim('test_sd.mdl')
values = model.run()
values.head(5)