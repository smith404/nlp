package com.k2.tikaserver.controller;

import com.k2.tikaserver.TiKaUtils;
import com.k2.tikaserver.model.DocMetaData;
import com.k2.tikaserver.model.TextResponse;
import com.k2.tikaserver.service.UtilsService;
import com.k2.tikaserver.exception.BaseException;
import org.apache.tika.metadata.Metadata;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/tika")
public class TikaController
{
    @RequestMapping(method = RequestMethod.POST, value = "/gettext")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file,
                                        @RequestParam(value = "type", required = false, defaultValue = "content") String type,
                                        @RequestParam(value = "raw", required = false, defaultValue = "no") String raw, Model model)
    {
        List<DocMetaData> dmdList = new ArrayList<>();
        TextResponse tr = new TextResponse();
        boolean asList = false;

        try
        {
            if (file != null)
            {
                String fileName = file.getOriginalFilename();
                InputStream is = new ByteArrayInputStream(file.getBytes());

                if (type.equalsIgnoreCase("metadatalist"))
                {
                    asList = true;
                    Metadata theData = TiKaUtils.extractMetaDataUsingParser(is);
                    for(String name : theData.names())
                    {
                        DocMetaData dmd = new DocMetaData(name, theData.get(name));
                        dmdList.add(dmd);
                    }

                }
                else
                {
                    if (type.equalsIgnoreCase("metadata"))
                    {
                        Metadata theData = TiKaUtils.extractMetaDataUsingParser(is);
                        StringBuilder sb = new StringBuilder();
                        for(String name : theData.names())
                        {
                            DocMetaData dmd = new DocMetaData(name, theData.get(name));
                            sb.append(dmd.prettyPrint()).append(UtilsService.NEWLINE);
                        }
                        tr.setProperties(sb.toString());

                        is.reset();
                    }

                    String content;

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

                if (asList)
                    return new ResponseEntity<>(dmdList, HttpStatus.OK);
                else
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
