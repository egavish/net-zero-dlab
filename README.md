# net-zero-dlab

A place to share code and collaborate in the D-Lab net-zero emissions buildings project!

Notes from Amro about next steps for the code:
## Sustainability Data Pool:
- [x] ~Comment your code so that a Python-newbie can follow the general steps of your code.~
- [x] ~Begin to clean the data. Fill in missing and aberrant values.~
- [x] ~Add physical units to your plots~
- [x] ~Add labeled axes and legends where appropriate.~
- [x] ~Add more years so that you can see the annual cyclicity more than once~
- [x] ~Integrate all of your code into a single one-stop-shop Jupyter notebook. Later, you will be able to convert your jupyter notebook automatically into a webpage.~
- [x] ~Create figure captions to Interpret the "story" of the data. The best way to do this is to use markdown cells in your Jupyter notebook that follow each of your figures. What do you want your audience to know? What is important?~
- [x] ~Make sure there is a set of Choropleth maps on an absolute energy basis (e.g. kWh units) -- This should give you a sense of the buildings relative energy consumption~
- [ ] What can you say about the absolute energy consumption of each building relative to another? Why do you think that is the case?
- [x] ~Make a new set of Choropleth maps on a normalized per square foot basis (e.g. kWh/sq. ft).~
- [ ] What can you say about the specific energy consumption of each building relative to another? Why do you think that is the case?
- [x] ~Make a new set of Choropleth maps where the energy consumption of each building is normalized by its own maximum consumption.~
- [x] ~What does this tell you about the seasonality of the energy consumption?~
- [ ] For electricity, chilled water, and steam, make a new set of static histogram plots so that the x axis is the building number and the y-axis is total annual consumption (not normalized). Make sure to rank order the buildings from largest to smallest.
- [ ] Now do the same for peak/max monthly consumption (not normalized).
- [ ] Now do the same for min/monthly consumption (not normalized).
- [ ] Now do the same for the standard deviation (not normalized)
- [ ] Combine the above plots so that electricity, chilled water, and steam are on the same plot. x-axis is a building number with some reasonable choice of rank order. y-axis is the three types of energy carriers. z-axis is energy with a common set of units.
- [ ] Please be sure to document how you did the unit conversion in your notebook.
- [ ] Please share the PDF result with all of us so that we can comment on it for the next iteration.

## Daisys 2021 Data:
- [ ] For each building make a subplot that shows steam, chilled water, and electricity as a function of time.
- [ ] Comment on your observations.
- [ ] For each building make a subplot that shows steam, chilled water, and electricity as a duration curve. This is the same as the step immediately above but the data has been ranked from largest to smallest.  The x-axis should be labelled as percent of the year.  
- [ ] What size "storage device" of heat, chilled water, and electricity would you need for each building so that the duration curve is flat?
- [ ] Where are the inflection points of the duration curve? (Remember from calculus that the inflection point of a function is where the function's second derivative equals zero.). Why are the inflection points important?
- [ ] For each building make a subplot that shows steam, chilled water, and electricity as a histogram.
- [ ] Please calculate important statistics. Max, Min, standard deviation, mean, and total.
- [ ] For each building make a subplot that shows the power spectra. you will need to take the Fourier transform of the data.
- [ ] What frequencies are most dominant? What does this tell you?
