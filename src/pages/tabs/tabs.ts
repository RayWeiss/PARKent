import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';

// import { MapPage } from '../map/map';
// import { ListPage } from '../list/list';

@IonicPage(
{
  name: 'TabsPage'
})

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = 'MapPage';
  tab2Root = 'ListPage';

  constructor() {
  }
}
