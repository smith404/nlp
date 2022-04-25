import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Clause } from '../clause';

import { TextResponse } from '../text-response';

@Component({
  selector: 'app-doc-clause',
  templateUrl: './doc-clause.component.html',
  styleUrls: ['./doc-clause.component.css']
})
export class DocClauseComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  /**
   * active card indicator
   */
  _active = false;
  @Input()
   set active(active: boolean) {
    this._active =  active;
  }

  /**
   * The clause this component displays
   */
  _clause = new Clause();

  @Input()
   set clause(clause: Clause) {
    this._clause =  clause;
  }
}
