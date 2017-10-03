import { Component } from '@angular/core';

import { MapPage } from '../map/map';
import { ListPage } from '../list/list';


@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = MapPage;
  tab2Root = ListPage;

  constructor() {

  }
}
