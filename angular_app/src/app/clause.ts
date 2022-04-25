import { Span } from './span';

export class Clause {

    type: string = "";
    subtype: string = "";

    /**
     * Main text of the clause
     */
    body: string = "";

    /**
     * List of spans detected in the clause
     */
    spans: Span[] = [];
  
    constructor(data: Partial<Clause> = {}) {
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
  