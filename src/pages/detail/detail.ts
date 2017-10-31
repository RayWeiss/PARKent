import { Component, ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams, Slides } from 'ionic-angular';
import { Chart } from 'chart.js';

//general variables
var chartType = 'bar';
var xLabel = ["9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm","9pm"]
var legendLabel = "Predicted % Full";

//data for each chart
var mondayPercentFull = [15,35,38,47,55,80,82,65,50,45,32,22,18]
var tuesdayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]
var wednesdayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]
var thursdayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]
var fridayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]
var saturdayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]
var sundayPercentFull = [18,13,35,38,47,55,80,82,65,50,45,32,22]

//color of each chart
var blue = "rgb(77, 148, 255)";
// var mondayColor = "rgb(77, 148, 255)";
// var tuesdayColor = "rgb(78, 230, 99)";
// var wednesdayColor = "rgb(215, 230, 78)";
// var thursdayColor = "rgb(230, 176, 78)";
// var fridayColor = "rgb(230, 82, 78)";
// var saturdayColor = "rgb(230, 78, 199)";
// var sundayColor = "rgb(200, 78, 230)";

Chart.defaults.global.maintainAspectRatio = true;

@IonicPage({
  name: 'DetailPage'
})
@Component({
  selector: 'page-detail',
  templateUrl: 'detail.html',
})

export class DetailPage {
  @ViewChild(Slides) slide: Slides;
  @ViewChild('mondayChart') mondayChart;
  @ViewChild('tuesdayChart') tuesdayChart;
  @ViewChild('wednesdayChart') wednesdayChart;
  @ViewChild('thursdayChart') thursdayChart;
  @ViewChild('fridayChart') fridayChart;
  @ViewChild('saturdayChart') saturdayChart;
  @ViewChild('sundayChart') sundayChart;

  barChart: any;
  lot: any;
  item: any;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.item = navParams.get('item');
    this.barChart = ["mondayChart", "tuesdayChart", "wednesdayChart", "thursdayChart", "fridayChart", "saturdayChart", "sundayChart"];
    this.lot = [this.item.lotName];
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad DetailPage');
    this.initializeCharts();
  }

  initializeCharts() {
    //Monday
    this.mondayChart = new Chart(this.mondayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: mondayPercentFull,
          label: legendLabel,
          backgroundColor: blue,
        }]
      }
    }),

    //Tuesday
    this.tuesdayChart = new Chart(this.tuesdayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: tuesdayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Wednesday
    this.wednesdayChart = new Chart(this.wednesdayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: wednesdayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Thursday
    this.thursdayChart = new Chart(this.thursdayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: thursdayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Friday
    this.fridayChart = new Chart(this.fridayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: fridayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    }),

    //Saturday
    this.saturdayChart = new Chart(this.saturdayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: saturdayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    });

    //Sunday
    this.sundayChart = new Chart(this.sundayChart.nativeElement, {
      type: chartType,
      data: {
        labels: xLabel,
        datasets: [{
          data: sundayPercentFull,
          label: legendLabel,
          backgroundColor: blue
        }]
      }
    });
  }

}
