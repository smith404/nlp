import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http'

import { TextResponse } from './text-response';
import { Category } from './category';
import { Prediction } from './prediction';
import { NamedEntity } from './named-entity';
import { Span } from './span';
import { Clause } from './clause';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})

@Injectable()
export class AppComponent {

  /**
   * Store any bearer token 
   */
   bearerToken: string  = "***";

  /**
   * Simple text branding
   */
  brand: string = "Nemesis";

  /**
   * Sidebar status
   */
  opened: boolean = false;

  /**
   * Selected filename for display purposes only 
   */
  fileName: string = '';
  stuff: string = '';
  type: string = 'Legal Clause';
  subtype: string = 'Confidentiality';
  

  /**
   * The response represnetation of the file uploaded
   */
  uploadedFile: TextResponse = new TextResponse();

  /**
   * The list of categorizers and models
   */
  categorizers: Category[] = [];
  models: Category[] = [];
  selectedModels: Category[] = [];
  selectedCategory: Category = {id: 0, fullName:"", type: "", name:"", lang:""};

  /**
   * Variables associated with the tag elements
   */
  visible = true;
  selectable = true;
  removable = true;

  /**
   * Name to register new category under
   */
  categoryName: string = "";

  /**
   * 
   * @param http - the injected http client
   */
  constructor(private http: HttpClient, private snackBar: MatSnackBar) {

    this.http.get<Category[]>("http://localhost:8080/nlp/doc/nlp/categorizers").subscribe(data => {
      this.categorizers = data
      if (this.categorizers.length > 0) this.selectedCategory = this.categorizers[0];

  });
    this.http.get<Category[]>("http://localhost:8080/nlp/doc/nlp/models").subscribe(data => this.models = data);

  }

  openSnackBar(message: string, action: string, duration: number) {
    let snackBarRef = this.snackBar.open(message, action, { 'duration': duration });

    console.log("[" + this.stuff + "]");
    this.stuff = "Boo";

    snackBarRef.afterDismissed().subscribe(() => {
      //console.log('Dismissed');
    });

    snackBarRef.onAction().subscribe(() => {
      //console.log('Action triggered');
    })

  }

  testEvent(event: any) {
    console.log(event);
  }


  onMetaDataSelected(event: any) {
    if (this.readMetaData)
    {
      this.autoRemoveWhiteSpace = false;
      this.autoSingleTrimmedLine = false;  
      this.autoRemoveDuplicateBlankLines = false;  
      this. autoMakeAlphaNumeric = false;
    }
  }

  onOtherSelected(event: any) {
    if (this.autoRemoveWhiteSpace
      || this.autoSingleTrimmedLine
      || this.autoRemoveDuplicateBlankLines
      || this.autoMakeAlphaNumeric)
    {
      this.readMetaData  = false;
    }
  }  

  /**
   * Flag to indicate if spinner should be displayed
   */
  loading = false;
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
        this.uploadedFile = new TextResponse(data)
        this.clearDocumentTags();
      }, error => console.log('Error Caught', error))
      .add(() => { this.loading = false; });
    }

  }
  
  predictions: Prediction[] = [];
  minProbability: number = 0;

  /**
   * Filter method to determine if an entity should be displayed
   * @param element - the element to check
   * @returns true if the entity should be displayed else false
   */
  isApplicableEntity(element: NamedEntity) {
    let found = false;

    this.selectedModels.forEach(model => {
      if (model.name === element.name) found = true;
    })

    return found && (element.probability >= (this.minProbability / 100)); 
  } 
           
  diplayedNamedEntities: NamedEntity[] = [];
  namedEntities: NamedEntity[] = [];
  onFilterEntityResults() {
    this.diplayedNamedEntities = this.namedEntities.filter(entity => this.isApplicableEntity(entity));
  }

  displayedCategoryColumns: string[] = ['model', 'category', 'probability'];
  displayedEntityColumns: string[] = ['type', 'name', 'value', 'probability'];

  formatLabel(value: number) {
      return value + '%';
  }

  isTrainingMode = false;
  onModelCatClick() {
    if (this.isTrainingMode)
      this.onCreateCatModel();
    else
      this.onUseCatModel();
  }

  onClearNERText() {
    this.categoryName = "";
    this.uploadedFile.foot = "";
    this.predictions = [];
  }

  onClearCatText() {
    this.categoryName = "";
    this.uploadedFile.head = "";
    this.predictions = [];
  }

  onUseEntityModel() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `Bearer ${this.bearerToken}`
      })
    };

    this.http.post<NamedEntity[]>("http://localhost:8080/nlp/doc/nlp/nerdetect", this.uploadedFile.foot, httpOptions)
    .subscribe(data => {
      this.namedEntities = data;
      this.onFilterEntityResults()
    }, error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
}

clauses:Clause[] =  []

onToClauses() {
  const httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'text/html',
      'Access-Control-Allow-Origin': '*',
      'Authorization': `Bearer ${this.bearerToken}`
    })
  };

  this.http.post<Clause[]>("http://localhost:8080/nlp/doc/nlp/clauses", this.uploadedFile.foot, httpOptions)
  .subscribe(data => {

    this.clauses = data;
  }, error => console.log('Error Caught', error))
  .add(() => { this.loading = false; });
}

  getSentences() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
      })
    };

    this.http.post<Span[]>("http://localhost:8080/nlp/doc/sentences", this.uploadedFile.body, httpOptions)
    .subscribe(data => {
      let res: string = "";
      data.forEach(record => {
        res = res + this.uploadedFile.body.substring(record.start, record.end) + "\n";
      });

      this.uploadedFile.body = res;
    }, error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
  }

  getTokens() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
      })
    };

    this.http.post<Span[]>("http://localhost:8080/nlp/doc/tokens", this.uploadedFile.body, httpOptions)
    .subscribe(data => {
      console.log(data);
    }, error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
  }

  onUseCatModel() {
        const httpOptions = {
          headers: new HttpHeaders({
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
          })
        };

        this.http.post<Prediction[]>("http://localhost:8080/nlp/doc/nlp/classify?category=" + this.selectedCategory.lang + "-" + this.selectedCategory.name, this.uploadedFile.head, httpOptions)
        .subscribe(data => this.predictions = data, error => console.log('Error Caught', error))
        .add(() => { this.loading = false; });
  }

  onCreateCatModel() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
      })
    };

    this.http.post<TextResponse>("http://localhost:8080/nlp/doc/newCatModel?name=bla", this.uploadedFile.head, httpOptions)
    .subscribe(data => this.openSnackBar("New Category Model Created","Dismiss", 5000), error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
  }

  onCreateNERModel() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
      })
    };

    this.http.post<TextResponse>("http://localhost:8080/nlp/doc/newEntityModel?name=bla", this.uploadedFile.foot, httpOptions)
    .subscribe(data => this.openSnackBar("New Entity Model Created","Dismiss", 5000), error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
  }


  /**
   * Properties for file loading
   */
  readMetaData: boolean = false;
  autoRemoveWhiteSpace: boolean = false;
  autoRemoveDuplicateBlankLines: boolean = true;  
  autoMakeAlphaNumeric: boolean = true;
  autoSingleTrimmedLine: boolean = false;  

  tagDocument() {

    this.loading = true;

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
      })
    };

    this.http.post<NamedEntity[]>("http://localhost:8080/nlp/doc/nlp/nerdetect?tolerance=" + this.minProbability, this.uploadedFile.body, httpOptions)
    .subscribe(data => {
      data.forEach(tag => this.addDocumentTags(tag))
      this.loading = false;
    }, error => console.log('Error Caught', error))
    .add(() => { this.loading = false; });
  }

  /**
   * Helper method to clear tag list
   */
  clearDocumentTags() {
    this.docTags = [];
  }

  /**
   * The tag list for the currently uploaded document
   */
  docTags: NamedEntity[] = [];

  /**
   * Remove the tag object from the tag list
   * @param tag - the object to remove
   */
  removeDocumentTag(tag: NamedEntity) {
    const index = this.docTags.indexOf(tag);

    if (index >= 0) {
      this.docTags.splice(index, 1);
    }
  }

  /**
   * Add a document tag only if the value of the tag is not already in the list
   * @param tag - the tag to add
   */
  addDocumentTags(tag: NamedEntity) {
    const found = this.docTags.find(element => element.value.localeCompare(tag.value)==0);

    if (!found) this.docTags.push(tag);
  }

  tagNER(elementName: string)
        {
            const tag = "Planet";
            const txtArea = <HTMLInputElement> document.getElementById(elementName);

            let start = txtArea.selectionStart ? txtArea.selectionStart : 0;
            let finish = txtArea.selectionEnd ? txtArea.selectionEnd : 0;

            // If nothing selected just return
            if (start == finish) return;

            let rawSel = txtArea.value.substring(start, finish);
            let sel = rawSel.trim();
            if (sel.length != rawSel.length)
            {
              let startPos = rawSel.search(sel);
                if (startPos == 0)
                {
                    finish = finish - (rawSel.length - sel.length);
                }
                if (startPos > 0)
                {
                    start = start + startPos;
                    finish = start + sel.length;
                }
            }

            var before = txtArea.value.substring(0, start);
            var after = txtArea.value.substring(finish);
            sel = '<START:' + tag + '>' + sel + '<END>';

            this.uploadedFile.foot = before + sel + after;
       }
}


