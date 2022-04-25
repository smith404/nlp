import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http'

import { TextResponse } from '../text-response';

@Component({
  selector: 'app-file-loader',
  templateUrl: './file-loader.component.html',
  styleUrls: ['./file-loader.component.css']
})
export class FileLoaderComponent implements OnInit {

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  /**
   * Selected filename for display purposes only 
   */
   fileName: string = '';

 /**
   * Flag to indicate if spinner should be displayed
   */
  loading = false;

  /**
   * The response represnetation of the file uploaded
   */
  @Input()
   set content(content: string) {
    this._response.body = content || '';
  }
  @Output() contentChange = new EventEmitter<string>();

   _response = new TextResponse();

  onFileSelected(event: any) {
    const file:File = event.target.files[0];

    if (file) {
      this.loading = true;
      this.fileName = file.name;

      const formData = new FormData();

      formData.append("file", file, file.name);

      const httpOptions = {
        headers: new HttpHeaders({
          'Access-Control-Allow-Origin': '*'
        })
      };

      this.http.post<TextResponse>("http://localhost:8080/nlp/doc/upload", formData, httpOptions)
      .subscribe(data => {
        this._response.body = data.body;
        this._response.head = data.head;
        this._response.foot = data.foot;
        this.contentChange.emit(this._response.body);

      }, error => console.log('Error Caught', error))
      .add(() => { this.loading = false; });
    }

  }  
}
