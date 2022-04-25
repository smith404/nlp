export class TextResponse {

  head: string = "";
  body: string = "";
  foot: string = "";

  constructor(data: Partial<TextResponse> = {}) {
    Object.assign(this, data);
  }

  removeWhiteSpace() {
      this.body = this.body.replace(/[\n\r]/g, '');
  }
  
  singleTrimmedLine() {
    this.body = this.body.replace(/\n/g, ' ');
    this.body = this.body.replace(/\s\s+/g, ' ');
  }   
  
  removeDuplicateBlankLines() {
    this.body = this.body.replace(/[\r\n]\s*[\r\n]/g, '\n\n');
  }   
  
  makeAlphaNumeric() {
    this.body = this.body.replace(/[^a-z0-9 ]/gi,'');
  }
  
}
