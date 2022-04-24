/*
 * Copyright (c) 2021. K2-Software
 * All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.model;

import java.util.ArrayList;
import java.util.List;

public class TextResponse
{
    private String result;
    private boolean success;
    private List<CustomPair> properties;

    public TextResponse()
    {
        result = "";
        success = true;
        properties = new ArrayList<>();
    }

    public String getResult()
    {
        return result;
    }

    public void setResult(String result)
    {
        this.result = result;
    }

    public boolean isSuccess()
    {
        return success;
    }

    public void setSuccess(boolean sucess)
    {
        this.success = sucess;
    }

    public List<CustomPair> getProperties()
    {
        return properties;
    }

    public void setProperties(List<CustomPair> properties)
    {
        this.properties = properties;
    }

    @Override
    public String toString()
    {
        return "TextResponse{" +
                "result='" + result + '\'' +
                ", success=" + success +
                ", properties='" + properties + '\'' +
                '}';
    }
}
