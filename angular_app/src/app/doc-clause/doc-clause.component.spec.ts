import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocClauseComponent } from './doc-clause.component';

describe('DocClauseComponent', () => {
  let component: DocClauseComponent;
  let fixture: ComponentFixture<DocClauseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DocClauseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DocClauseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
