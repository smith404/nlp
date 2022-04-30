/*
 * Copyright (c) 2022. All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.
 */

package com.k2.tikaserver.controller;

import com.k2.tikaserver.TiKaUtils;
import com.k2.tikaserver.exception.BaseException;
import com.k2.tikaserver.model.CustomPair;
import com.k2.tikaserver.model.TextResponse;
import com.k2.tikaserver.service.UtilsService;
import org.apache.tika.metadata.Metadata;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.InputStream;

@RestController
@RequestMapping("/tika")
public class TikaController
{
    @RequestMapping(method = RequestMethod.POST, value = "/gettext")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file,
                                        @RequestParam(value = "type", required = false, defaultValue = "content") String type,
                                        @RequestParam(value = "raw", required = false, defaultValue = "no") String raw, Model model)
    {
        TextResponse tr = new TextResponse();

        try
        {
            if (file != null)
            {
                String fileName = file.getOriginalFilename();
                InputStream is = new ByteArrayInputStream(file.getBytes());

                {
                    String content = "";
                    Metadata theData = TiKaUtils.extractMetaDataUsingParser(is);
                    StringBuilder sb = new StringBuilder();
                    for (String name : theData.names())
                    {
                        CustomPair pair = new CustomPair(name, theData.get(name));
                        tr.getProperties().add(pair);
                    }
                    is.reset();

                    if (TiKaUtils.IsImageExtension(fileName))
                    {
                        content = TiKaUtils.extractJpgContentUsingOCR(is);
                    }
                    else
                    {
                        content = TiKaUtils.extractContentUsingParser(is);
                    }

                    if (content.trim().length() == 0 && fileName.endsWith("pdf"))
                    {
                        is.reset();
                        content = TiKaUtils.extractPdfContentUsingOCR(is);
                    }

                    if (type.equalsIgnoreCase("concat"))
                    {
                        content = content.replaceAll("(\\r|\\n)", (UtilsService.SPACE));
                        content = content.replaceAll("\\s{2,}", (UtilsService.SPACE)).trim();
                        if (!raw.equalsIgnoreCase("yes")) content = content.replaceAll("/[^A-Za-z0-9 ]/", "");
                    }
                    tr.setResult(content);
                }

                is.close();

                return new ResponseEntity<>(tr, HttpStatus.OK);
            }

            return new ResponseEntity<>(tr, HttpStatus.NO_CONTENT);
        }
        catch (Exception ex)
        {
            throw new BaseException(ex.getMessage(), ex);
        }
    }
}
