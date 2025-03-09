# Asteroid Mining with LLMs

Asteroid mining is hard, it is harder if you cannot find what you are looking for. In this exercise, I will take a locally ([M2 Pro 16GB 512GB](https://support.apple.com/en-us/111837)) running a Large Language Model, [IBM granite3.1-dense:8b](https://www.ollama.com/library/granite3.1-dense), via [Ollama](https://ollama.com) to classify asteroids and elements so that we can easily answer the following question.

```
How much is an asteroid worth?
```

Based on it's class, it will likely contain certain elements.  Some metallic class asteroids are known to have high concentrations of [platinum group metals](https://en.wikipedia.org/wiki/Platinum_group). Platinums value is over [$900+ per oz](https://finance.yahoo.com/quote/PL=F/)!

### Classifying Asteroids

With a collection of [958524 asteroids, thanks to https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset](https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset), it is important for my use case that they have a `class` of either `C` (Carbonaceous), `S` (Silicaceous), `M` (Metallic), or `O` (Other, unclassified). 

### Elements

119 Elements in the periodic table, we have all the information you could imagine on elements thanks to [https://github.com/Bowserinator/Periodic-Table-JSON](https://github.com/Bowserinator/Periodic-Table-JSON).  

I needed to make sure the usecases benefited space exploration. 12 usecases that could easily overlap several of the 119 elements.

`"fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"`

I also wanted to show the likelihood of each element appearing in each class of asteroid [`C`, `S`, and `M`]. I used Pydantic and Ollama to read each element and update its document with its uses and classes.

