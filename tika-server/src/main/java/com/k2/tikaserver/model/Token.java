/*
 * Copyright (c) 2021-2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.model;

import opennlp.tools.util.Span;

import java.util.UUID;

public class Token
{
    private static long idCounter = 0;

    private UUID id = UUID.randomUUID();

    private String type;

    private String lemma;

    private String value;

    private double probability;

    private int start;

    private int length;

    private int end;

    public Token()
    {
        type = "";
        lemma = "";
        value = "";
        probability = 0D;
        start = 0;
        length = 0;
    }

    public Token(Token that)
    {
        this.type = that.type;
        this.lemma = that.lemma;
        this.value = that.value;
        this.probability = that.probability;
        this.start = that.start;
        this.length = that.length;
    }

    public Token(Span span, String value)
    {
        this.type = (span.getType() == null) ? "UNKNOWN" : span.getType();
        this.lemma = "";
        this.value = value;
        this.start = span.getStart();
        this.length = span.length();
        this.probability = span.getProb();
    }

    public Token(Span span, String value, String type)
    {
        this.type = (span.getType() == null) ? type : span.getType();
        this.lemma = "";
        this.value = value;
        this.start = span.getStart();
        this.length = span.length();
        this.probability = span.getProb();
    }

    public Token(Span span, String value, String lemma, String type)
    {
        this.type = (span.getType() == null) ? type : span.getType();
        this.lemma = lemma;
        this.value = value;
        this.start = span.getStart();
        this.length = span.length();
        this.probability = span.getProb();
    }

    public Token(String type, String value, double probability, int start, int length)
    {
        this.type = type;
        this.lemma = "";
        this.value = value;
        this.probability = probability;
        this.start = start;
        this.length = length;
    }

    public UUID getId()
    {
        return id;
    }

    public String getType()
    {
        return type;
    }

    public void setType(String type)
    {
        this.type = type;
    }

    public String getValue()
    {
        return value;
    }

    public void setValue(String value)
    {
        this.value = value;
    }

    public double getProbability()
    {
        return probability;
    }

    public void setProbability(double probability)
    {
        this.probability = probability;
    }

    public int getStart()
    {
        return start;
    }

    public void setStart(int start)
    {
        this.start = start;
    }

    public int getLength()
    {
        return length;
    }

    public void setLength(int length)
    {
        this.length = length;
    }

    public String getLemma()
    {
        return lemma;
    }

    public void setLemma(String lemma)
    {
        this.lemma = lemma;
    }

    public boolean better(Token that)
    {
        return (this.probability >= that.probability);
    }

    public int getEnd()
    {
        return this.start + this.length;
    }

    @Override
    public String toString()
    {
        return "NamedEntity{" +
                ", type='" + type + '\'' +
                ", value='" + value + '\'' +
                ", probability=" + probability +
                ", start=" + start +
                ", length=" + length +
                '}';
    }

    @Override
    public int hashCode()
    {
        return super.hashCode();
    }

    @Override
    public boolean equals(Object obj)
    {
        if (!(obj instanceof Token)) return false;

        Token that = (Token) obj;
        return (this.start == that.start && this.length == that.length && this.probability == that.probability);
    }
}
