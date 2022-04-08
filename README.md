# net-zero-dlab

A place to share code and collaborate in the D-Lab net-zero emissions buildings project!


Notes from Amro about next steps for the code:
1. Comment your code so that a Python-newbie can follow the general steps of your code.
2. Begin to clean the data. Fill in missing and aberrant values.
3. Add physical units to your plots
4. Add labeled axes and legends where appropriate.
5. Add more years so that you can see the annual cyclicity more than once
6. Integrate all of your code into a single one-stop-shop Jupyter notebook. Later, you will be able to convert your jupyter notebook automatically into a webpage.
7. Create figure captions to Interpret the "story" of the data. The best way to do this is to use markdown cells in your Jupyter notebook that follow each of your figures. What do you want your audience to know? What is important?
8. Make sure there is a set of Choropleth maps on an absolute energy basis (e.g. kWh units) -- This should give you a sense of the buildings relative energy consumption
9. What can you say about the absolute energy consumption of each building relative to another? Why do you think that is the case?
10. Make a new set of Choropleth maps on a normalized per square foot basis (e.g. kWh/sq. ft).
11. What can you say about the specific energy consumption of each building relative to another? Why do you think that is the case?
12. Make a new set of Choropleth maps where the energy consumption of each building is normalized by its own maximum consumption.
13. What does this tell you about the seasonality of the energy consumption?
14. For electricity, chilled water, and steam, make a new set of static histogram plots so that the x axis is the building number and the y-axis is total annual consumption (not normalized). Make sure to rank order the buildings from largest to smallest.
15. Now do the same for peak/max monthly consumption (not normalized).
16. Now do the same for min/monthly consumption (not normalized).
17. Now do the same for the standard deviation (not normalized)
18. Combine the above plots so that electricity, chilled water, and steam are on the same plot. x-axis is a building number with some reasonable choice of rank order. y-axis is the three types of energy carriers. z-axis is energy with a common set of units.
19. Please be sure to document how you did the unit conversion in your notebook.
20. Please share the PDF result with all of us so that we can comment on it for the next iteration.
