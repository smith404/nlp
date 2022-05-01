/*
 * Copyright (c) 2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.service;

import com.k2.tikaserver.model.Prediction;
import com.k2.tikaserver.model.Token;
import opennlp.tools.util.Span;

import java.util.List;

public interface NLPService
{
    Prediction detectLanguage(String text);

    List<String> stopWords();

    String[] sentences(String text);

    Span[] sentencesPos(String text);

    Token[] sentencesValues(String text);

    String[] tokenize(String text);

    Span[] tokenizePos(String text);

    Token[] tokenizeValues(String text);

    String[] tags(String[] tokens);

    String[] lemmas(String[] tokens, String[] tags);

    String[] chunks(String[] tokens, String[] tags);

    List<Token> splitClauses(String text);

    List<Token> sanitize(String text);

    String toSanitizedString(String text);
}
