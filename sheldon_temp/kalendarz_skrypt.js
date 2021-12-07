function isLeapYear(year)
{
	return (year%4==0 && year%100!=0) ||  (year%400 == 0)
}

function generateCalendarCells(month,year)
{
	const monthLengths = [31,28,31,30,31,30,31,31,30,31,30,31];
	if (isLeapYear(year)) monthLengths[1] = 29;
	const firstDay = new Date(year,month,1);
	const firstWeekday = firstDay.getDay();
	const calendarCells = [...document.querySelectorAll('.calendar-cell')];
	let count = 0;
	let dayCount = 1;
	calendarCells.forEach((cell)=>{
		if (count>=firstWeekday && count<firstWeekday+monthLengths[month])
		{
			cell.innerText = dayCount;
			cell.classList.add('calendar-cell-active');
			cell.classList.remove('calendar-cell-inactive');
			dayCount++;
		}
		else
		{
			cell.innerText = '';
			cell.classList.add('calendar-cell-inactive');
			cell.classList.remove('calendar-cell-active');
		}
		count++;
	});
}

function getDayString(date)
{
	var formatter = new Intl.DateTimeFormat( 'pl', {
	day: 'numeric',
	month: 'long',
	year: 'numeric'
} );
const a = formatter.format( date );
return a.toString();
	//const monthnames_polish_case = ['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia'];
	//return d.toString()+' '+monthnames_polish_case[m]+' '+y.toString();
}

function getlabel(i,r)
{
	r = r%24;
	return (i<=9?'0':'')+i.toString()+':00-'+(r<=9?'0':'')+(r).toString()+':00';
}

function printList(list)
{
	list.sort(function(a,b){
		if (a.date<b.date) return -1;
		if (b.date<a.date) return 1;

		if (a.time<b.time) return -1;
		if (b.time<a.time) return 1;
		return 0;
	});
	const htmllist = document.getElementById('chosentimelist');
	htmllist.textContent = '';
	let i = 0;
	while(i < list.length)
	{
		const daylist = list.filter((el)=>{
			return el.date.getTime()==list[i].date.getTime();
		});
		const timesarr = [];
		daylist.forEach((el)=>timesarr.push(el.time));
		const li = document.createElement('li');
		li.innerText+=`${getDayString(list[i].date)}, godziny: `;
		let start = timesarr[0];
		let end = timesarr[0]+1;
		let k = 1;
		for (let i = 0 ; i < timesarr.length; i++)
		{
			li.innerText += getlabel(timesarr[i],timesarr[i]+1)+',';
		}
		console.log(timesarr);
		console.log("");
		htmllist.appendChild(li);
		i+=daylist.length;
	}
}

function indexOfList(list,obj)
{
	for (let i = 0 ; i < list.length ; i++)
	{
		if (obj.date.getTime()==list[i].date.getTime() && obj.time == list[i].time) return i;
	}
	return -1;
}

function run()
{
	const month_input = document.getElementById('month-input');
	const year_input = document.getElementById('year-input');
	const dayheader = document.getElementById('calendar-day-header');

	generateCalendarCells(month_input.value,year_input.value);
	let calendarCells = document.querySelectorAll('calendar-cell-active');

	month_input.addEventListener('input',function()
	{
		generateCalendarCells(month_input.value,year_input.value);
	});
	year_input.addEventListener('input',function()
	{
		generateCalendarCells(month_input.value,year_input.value);
	});

	const now = new Date();
	month_input.value = now.getMonth();
	year_input.value = now.getFullYear();
	//let currentDay = {year:now.getFullYear(),month:now.getMonth(),day:now.getDate()};
	let currentDay = now;
	dayheader.innerText = getDayString(currentDay);

	const calview = document.getElementById('calendar-view');
	calview.addEventListener('click',function(e){
		if (e.target.classList.contains('calendar-cell-active'))
		{
			dayheader.innerText = getDayString(currentDay);
			//currentDay = {year:year_input.value,month:month_input.value,day:Number(e.target.innerText)};
			currentDay = new Date(year_input.value,month_input.value,Number(e.target.innerText));
		}
	});

	const calscheme = document.getElementById('calendar-day-scheme');
	const chosenlist = document.getElementById('chosentimelist');
	const chosentimelist = [];
	calscheme.addEventListener('click',function(e){
		if (e.target.classList.contains('scheme-cell-choosebtn'))
		{
			const el = e.target.parentNode;
			const timeobj = {date:currentDay,time:Number(el.getAttribute('value'))};
			const res = indexOfList(chosentimelist,timeobj);
			if (res>-1)
			{
				chosentimelist.splice(res,1);
				el.classList.remove('scheme-row-chosen');
			}
			else
			{
				chosentimelist.push(timeobj);
				el.classList.add('scheme-row-chosen');
			}
			printList(chosentimelist);
		}
	});

}

document.addEventListener('DOMContentLoaded',run);