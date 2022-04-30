package com.k2.tikaserver.model;

public class Clause
{
    private String body;

    private String type;

    private String subtype;

    public Clause()
    {
        body = "";
        type = "";
        subtype = "";
    }

    public String getBody()
    {
        return body;
    }

    public void setBody(String body)
    {
        this.body = body;
    }

    public String getType()
    {
        return type;
    }

    public void setType(String type)
    {
        this.type = type;
    }

    public String getSubtype()
    {
        return subtype;
    }

    public void setSubtype(String subtype)
    {
        this.subtype = subtype;
    }
}

