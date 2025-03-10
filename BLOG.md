# Asteroid Mining with LLMs

Asteroid mining is hard, it is harder if you cannot find what you are looking for. We are going to use low power hardware ([M2 Pro 16GB 512GB](https://support.apple.com/en-us/111837)) to run a Large Language Model, [IBM granite3.1-dense:8b](https://www.ollama.com/library/granite3.1-dense), via [Ollama](https://ollama.com) to classify asteroids and elements so that we can easily answer the following question.

> How much is an asteroid worth?

Based on it's class, it will likely contain certain elements.  Some M (Metallic) class asteroids are known to have high concentrations of [platinum group metals](https://en.wikipedia.org/wiki/Platinum_group). Platinums value is over [$900+ per oz](https://finance.yahoo.com/quote/PL=F/)!  To keep life simple I will be measuring all mining quantities in kilograms.  `35.27 oz in 1 kg. $900 x 35.27 oz = $31,743 per kg of platinum`. It's trading far above $900 at this moment so let's round up to $32k per 1 kg of Platinum.

### Classifying Asteroids

With a collection of [958524 asteroids, thanks to https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset](https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset), it is important for my use case that they have a `class` of either `C` (Carbonaceous), `S` (Silicaceous), `M` (Metallic), or `O` (Other, unclassified). 

### Element Uses

119 Elements in the periodic table, we have all the information you could imagine on elements thanks to [https://github.com/Bowserinator/Periodic-Table-JSON](https://github.com/Bowserinator/Periodic-Table-JSON).  

I wanted to know what usecases each element could be used for in the context of "benefits space exploration". 12 usecases that could easily overlap several of the 119 elements.

> `"fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"`

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

- Find the asteroid(s) closest to Earth measured in [Astronomical Units](https://en.wikipedia.org/wiki/Astronomical_unit)
- Estimate it's value
- Flight plan - estimate the total number of days to intersect, days to establish site, days to fill cargo to capacity, days to return (considering additional mass)
- Based on the value of the elements x capacity of cargo = mission value
- Send ship, survive, return with valuable resources, get paid.

## Where are you? [AU]
Key to finding anything in space is finding it's relation to something significant, like our SUN. The distance from Earth to the Sun is 1 Astronomical Unit. Each asteroid has a `moid` field which stands for [minimum orbital intersection distance measured in Astronomical Units](https://en.wikipedia.org/wiki/Minimum_orbit_intersection_distance) aka closest distance between the asteroid and Earth.  

For instance `Ceres` has a `moid` of `1.59478` AU.  1 AU is 149,597,871 km, so `Ceres` is 238,575,692 km from Earth at its closest point.

With the absolute latest in human engineering it's possible to get from [Earth to Mars in 45 days](https://www.iflscience.com/nuclear-thermal-propulsion-reactor-fuel-that-could-take-humans-to-mars-tested-at-nasa-facility-77719). The distance from Earth to Mars is 0.52 AU or 78,340,000 km. `78,340,000 km / 45 days =
1,740,889 km per day or 72,537 km per hour`. 

This means it would take us 137 days to get to the asteroid `Ceres`.

`238,575,692 km to Ceres / 1,740,889 km per day = 137 days`

## Mine, all mine
Due to `Ceres` size, it is fair to say that multiple mining sites could exist over this 939.4 km diameter asteroid.  It's mass is estimated to be 938,390,000,000,000,000,000 kg.

Based on this mass we are going to estimate that all other asteroids have a similar 998,924,845,646,000,000 kg of mass per 1 km of diameter.  

## Dig it

We are going to estimate our mining ship can extract 10,000 kg of material per hour or 240,000 kg of material per day based on [published surface mining data](https://www.eia.gov/coal/annual/pdf/tableES2.pdf).  In mining, **gangue** is the commercially worthless material that surrounds, or is closely mixed with, a wanted mineral in an ore deposit.  For example, say you have 10,000 kg of rock you have mined for platinum that has an ore grade of 10%. This means you only get 1,000 kg of platinum and 9,000 kg of gangue that you have to separate and get rid of (10% platinum ore would be very high grade). 

> 24,000 kg per day of useful elements if all goes well.

## Logistics and costs
The [Falcon Heavy](https://en.wikipedia.org/wiki/Falcon_Heavy) can lift 9,200 kg into space. We will be rounding that up to 10,000 kg. That's $320 million dollars in platinum.

The Falcon Heavy has 2 costs models; 
- Reusable: US $97 million
- Expendable: US$150 million

If your ship + cargo makes it back, great (minus several million in repairs)!  If it doesn't, it's going to cost $150 million to try again.

### Operational costs per day

- 137 days to Ceres. 

- 3 days to establish mining site.

- 1 day to mine.

- 1 day to prep for return.

- 137 days to Earth.

Piloted by 3 AIs to form a quorum will help ensure mission success. Each specializing in specific fields; 
- non-terrestrial mining operations
- astral navigation
- resource management

$45,000 per day based on a $16M+ annual run rate.  Play with those numbers as you would like.  279 days @ $45K per day is $12.5M total mission operational costs.

## TL;DR
**$150M** to launch, $50 million saved if you can reuse it for future missions.

**$12.5M** mission operation costs.

**$162.5M total investment.**

**$320M in recovered resources.**

# $157.5M in profits

Take that and invest in a 2nd shuttle. Repeat as needed.
