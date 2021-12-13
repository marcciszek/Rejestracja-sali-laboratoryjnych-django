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
		li.innerText+=`${getDayString(list[i].date)}, `;
		if (timesarr.length<24) 
		{
			li.innerText+='godziny: ';
			let s = timesarr[0];
			let e = timesarr[0]+1;
			for (let b = 0 ; b < timesarr.length ; b++)
			{
				s = timesarr[b];
				e = s+1;
				while(timesarr.indexOf(e)!=-1)
				{
					e++;
					b++;
				}
				li.innerText+=getlabel(s,e)+', ';
			}
		}
		else li.innerText+= ' (cały dzień)';
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
	let calendarCells = document.querySelectorAll('.calendar-cell-active');
	month_input.addEventListener('input',function()
	{
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	});
	year_input.addEventListener('input',function()
	{
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	});

	const nextbtn = document.getElementById('month-next-btn');
	const prevbtn = document.getElementById('month-prev-btn');

	nextbtn.addEventListener('click',function(e){
		e.preventDefault();
		let monthvalue = Number(month_input.value)+1;
		if (monthvalue>=12)
		{
			month_input.value = 0;
			year_input.value++;
		}
		else
		{
			month_input.value++;
		}
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	});

	prevbtn.addEventListener('click',function(e){
		e.preventDefault();
		let monthvalue = Number(month_input.value)-1;
		if (monthvalue<=0)
		{
			month_input.value = 11;
			year_input.value--;
		}
		else
		{
			month_input.value--;
		}
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	});

	const now = new Date();
	month_input.value = now.getMonth();
	year_input.value = now.getFullYear();
	let currentDay = new Date(now.getFullYear(),now.getMonth(),now.getDate());
	dayheader.innerText = getDayString(currentDay);
	calendarCells[currentDay.getDate()-1].classList.add('calendar-cell-current');
	const calview = document.getElementById('calendar-view');
	calview.addEventListener('click',function(e){
		if (e.target.classList.contains('calendar-cell-active'))
		{
			currentDay = new Date(year_input.value,month_input.value,Number(e.target.innerText));
			dayheader.innerText = getDayString(currentDay);
			[...document.getElementsByClassName('calendar-cell-current')].forEach((el)=>{
				el.classList.remove('calendar-cell-current');
			});
			e.target.classList.add('calendar-cell-current');
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