package com.k2.tikaserver.model;

public class Prediction
{
    private String model;

    private String category;

    private Double probability;

    public Prediction()
    {
        model = "";
        category = "";
        probability = 0D;
    }

    public String getModel()
    {
        return model;
    }

    public void setModel(String model)
    {
        this.model = model;
    }

    public String getCategory()
    {
        return category;
    }

    public void setCategory(String category)
    {
        this.category = category;
    }

    public Double getProbability()
    {
        return probability;
    }

    public void setProbability(Double probability)
    {
        this.probability = probability;
    }
}
