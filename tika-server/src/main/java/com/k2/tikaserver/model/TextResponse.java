/*
 * Copyright (c) 2021. K2-Software
 * All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.model;

public class TextResponse
{
    private String original;
    private String result;
    private boolean success;
    private String properties;

    public TextResponse()
    {
        original = "";
        result = "";
        success = true;
        properties = "";
    }

    public String getOriginal()
    {
        return original;
    }

    public void setOriginal(String original)
    {
        this.original = original;
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

    public String getProperties()
    {
        return properties;
    }

    public void setProperties(String properties)
    {
        this.properties = properties;
    }
}
