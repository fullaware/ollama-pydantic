# Asteroid Mining with LLMs

Asteroid mining is hard, it is harder if you cannot find what you are looking for. In this exercise, I will take a locally ([M2 Pro 16GB 512GB](https://support.apple.com/en-us/111837)) running a Large Language Model, [IBM granite3.1-dense:8b](https://www.ollama.com/library/granite3.1-dense), via [Ollama](https://ollama.com) to classify asteroids and elements so that we can easily answer the following question.

```
How much is an asteroid worth?
```

Based on it's class, it will likely contain certain elements.  Some metallic class asteroids are known to have high concentrations of [platinum group metals](https://en.wikipedia.org/wiki/Platinum_group). Platinums value is over [$900+ per oz](https://finance.yahoo.com/quote/PL=F/)!

### Classifying Asteroids

With a collection of [958524 asteroids, thanks to https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset](https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset), it is important for my use case that they have a `class` of either `C` (Carbonaceous), `S` (Silicaceous), `M` (Metallic), or `O` (Other, unclassified). 

### Element Uses

119 Elements in the periodic table, we have all the information you could imagine on elements thanks to [https://github.com/Bowserinator/Periodic-Table-JSON](https://github.com/Bowserinator/Periodic-Table-JSON).  

I wanted to know what usecases each element could be used for in the context of "benefits space exploration". 12 usecases that could easily overlap several of the 119 elements.

`"fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"`

I also wanted to show the likelihood of each element appearing in each class of asteroid [`C`, `S`, and `M`]. I used Pydantic and Ollama to read each element and update its document with its uses and classes.

For instance `Hydrogen` now has the following fields:

```
"uses": [
    "fuel",
    "energystorage",
    "industrial",
    "propulsion"
  ],
"classes": [
    {
      "class": "C",
      "percentage": 60
    },
    {
      "class": "S",
      "percentage": 35
    },
    {
      "class": "M",
      "percentage": 5
    }
  ]
```

# Let's go hunting!

- Find the asteroid(s) closest to us measured in [Astronomical Units](https://en.wikipedia.org/wiki/Astronomical_unit)
- Based on class, estimate it's value based on it's percentage of elements
- Flight plan - estimate the total number of days to intersect, days to establish site, days to fill cargo to capacity, days to return (considering additional mass)
- Based on the value of the elements x capacity of cargo = mission value

Key to finding anything in space is finding it's relation to something significant, like our SUN. `moid` is the [minimum orbital intersection distance measured in Astronomical Units](https://en.wikipedia.org/wiki/Minimum_orbit_intersection_distance) aka closest distance the asteroid is projected to be to Earth.  

For instance `Ceres` has a `moid` of `1.59478` AU.  1 AU is 149,597,871 km, so `Ceres` is 238,575,692 km from Earth at its closest point.
