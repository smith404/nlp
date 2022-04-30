/*
 * Copyright (c) 2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

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
