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
	let cellCount = 0;
	let dayCount = 1;
	calendarCells.forEach((cell)=>{
		if (cellCount>=firstWeekday && cellCount<firstWeekday+monthLengths[month])
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
		cellCount++;
	});
}

function getDayString(date)
{
	var formatter = new Intl.DateTimeFormat('pl',{
	day: 'numeric',
	month: 'long',
	year: 'numeric'
	});
const formatdate = formatter.format(date);
return formatdate.toString();
}

function getTimeIntervalLabel(i,r)
{
	r = r%24;
	return (i<=9?'0':'')+i.toString()+':00-'+(r<=9?'0':'')+(r).toString()+':00';
}

function insertTimeIntervalLabelsList(intervalsStringList)
{
	const htmllist = document.getElementById('chosentimelist');
    htmllist.textContent = '';
    const alert = document.getElementById('nothing-chosen-alert');
	if (intervalsStringList.length <= 0)
	{
	    alert.style.display = 'block';
	    return;
	}
	alert.style.display = 'none';
	intervalsStringList.forEach((text)=>{
		const li = document.createElement('li');
		li.innerText = text;
		htmllist.appendChild(li);
	});
}

function generateIntervalLabels(timesarr)
{
	let labelString = "";
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
		labelString+=getTimeIntervalLabel(s,e)+', ';
	}
	return labelString;
}

function generateIntervalString(intervalsListOfSingleDay)
{
	let intervalString = "";
	const timesarr = [];
	intervalsListOfSingleDay.forEach((el)=>timesarr.push(el.time));
	intervalString+=`${getDayString(intervalsListOfSingleDay[0].date)}, `;
	if (timesarr.length<24) 
		{
			intervalString+='godziny: ';
			intervalString+=generateIntervalLabels(timesarr);
		}
	else
		{
			intervalString += ' (cały dzień)';
		}
	return intervalString;
}

function sortByDateAscending(a,b)
{
	if (a.date<b.date) return -1;
	if (b.date<a.date) return 1;

	if (a.time<b.time) return -1;
	if (b.time<a.time) return 1;
	return 0;
}

function getIntervalLabelsList(intervalsList)
{
	intervalsList.sort(sortByDateAscending);
	let i = 0;
	const intervalsStringList = [];
	while(i < intervalsList.length)
	{
		const intervalsListOfSingleDay = intervalsList.filter((el)=>{
			return el.date.getTime()==intervalsList[i].date.getTime();
		});
		intervalsStringList.push(generateIntervalString(intervalsListOfSingleDay));
		i+=intervalsListOfSingleDay.length;
	}
	return intervalsStringList;
}

function indexOfList(list,obj)
{
	for (let i = 0 ; i < list.length ; i++)
	{
		if (obj.date.getTime()==list[i].date.getTime() && obj.time == list[i].time) return i;
	}
	return -1;
}

function handleClick_prevMonthBtn(monthCurrent,yearCurrent)
{
	if (--monthCurrent<0)
		{
			monthCurrent = 11;
			yearCurrent--;
		}
	return {month:monthCurrent,year:yearCurrent};
}

function handleClick_nextMonthBtn(monthCurrent,yearCurrent)
{
	if (++monthCurrent>=12)
		{
			monthCurrent = 0;
			yearCurrent++;
		}
	return {month:monthCurrent,year:yearCurrent};
}

function getOrderAlertText(labelList,message)
{
	let alertText = "Potwierdź wysłanie zamówienia na tę salę w poniższych przedziałach czasowych:\r\n\r\n";
	labelList.forEach((el)=>{
		alertText+=`${el}\r\n`;
	});
	alertText+=`\r\nWiadomość: ${message}`;
	return alertText;
}

function getSchemeCellContent(userslist)
{
	const aElementsList = [];
	if (userslist.length<=0) return '<span style="font-style:italic;">Wolne</span>';
	userslist.forEach((user)=>{
		aElementsList.push(`<a href=/user/${user}>${user}</a>&nbsp;`);
	});
	return aElementsList.join('');
}

function run()
{
	//REGION: Definitions

	const month_input = document.getElementById('month-input');
	const year_input = document.getElementById('year-input');
	const dayheader = document.getElementById('calendar-day-header');

	const nextbtn = document.getElementById('month-next-btn');
	const prevbtn = document.getElementById('month-prev-btn');

	const calview = document.getElementById('calendar-view');
	const calscheme = document.getElementById('calendar-day-scheme');
	const chosenlist = document.getElementById('chosentimelist');

	const ordersendbtn = document.getElementById('order-send');
	const orderMessageArea = document.getElementById('order-message');

	generateCalendarCells(month_input.value,year_input.value);

	let calendarCells = document.querySelectorAll('.calendar-cell-active');
	let currentDay;
	const chosentimelist = [];

	const calschemeCells = document.querySelectorAll('.scheme-row');
	calschemeCells[2].querySelector('.scheme-cell-content').insertAdjacentHTML('beforeend',getSchemeCellContent(["anna","maria","alek","gamon","fafefgwegw"]));
	calschemeCells[3].querySelector('.scheme-cell-content').insertAdjacentHTML('beforeend',getSchemeCellContent([]));
	//ENDREGION

	//REGION: Closures
	function handleMonthInput()
	{
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	}

	function handleSwitchingButtons(e,isNextBtnClicked)
	{
		e.preventDefault();
		let newMonth;
		if (isNextBtnClicked){newMonth = handleClick_nextMonthBtn(month_input.value,year_input.value);}
		else {newMonth = handleClick_prevMonthBtn(month_input.value,year_input.value);}
		month_input.value = newMonth.month;
		year_input.value = newMonth.year;
		generateCalendarCells(month_input.value,year_input.value);
		calendarCells = document.querySelectorAll('.calendar-cell-active');
	}

	function handleCalendarCellClick(e)
	{
		if (e.target.classList.contains('calendar-cell-active'))
		{
			currentDay = new Date(year_input.value,month_input.value,Number(e.target.innerText));
			dayheader.innerText = getDayString(currentDay);
			[...document.getElementsByClassName('calendar-cell-current')].forEach((el)=>{
				el.classList.remove('calendar-cell-current');
			});
			e.target.classList.add('calendar-cell-current');
		}
	}

	function handleCalendarSchemeClick(e)
	{
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
			insertTimeIntervalLabelsList(getIntervalLabelsList(chosentimelist));
		}
	}

	function getCSRFToken()
    {
      if (!document.cookie) return null;
      const arr = document.cookie.split(';').map((c)=>{return c.split('=')}).flat();
      return arr[arr.indexOf("csrftoken")+1];
    }

	function handleOrderSending(e)
	{
		e.preventDefault();
		if (confirm(getOrderAlertText(getIntervalLabelsList(chosentimelist),orderMessageArea.value)))
		{
			console.log("wszedlem do funkcji, gdzie generuje sie request post (fetch)");
			const data = { username: 'example' };
			const csrftoken = getCSRFToken();
            const headers = new Headers();
            headers.append('X-CSRFToken', csrftoken);
			fetch("test", {
			  method: 'POST',
              body: JSON.stringify(data),
              mode: 'same-origin',
			  headers: headers,
			  credentials: 'include'
			})
			.then(response => response.json())
			.then(data => {
			  console.log('Success:', data);
			  alert("Wysłano zamówienie.");
			})
			.catch((error) => {
			  console.error('Error:', error);
			});
		}
	}

	function setCurrentDayValues()
	{
		const now = new Date();
		month_input.value = now.getMonth();
		year_input.value = now.getFullYear();

		currentDay = new Date(now.getFullYear(),now.getMonth(),now.getDate());
		dayheader.innerText = getDayString(currentDay);
		calendarCells[currentDay.getDate()-1].classList.add('calendar-cell-current');
	}

	//ENDREGION

	//REGION: Event Listeners

	month_input.addEventListener('input',handleMonthInput);
	year_input.addEventListener('input',handleMonthInput);
	nextbtn.addEventListener('click',(e)=> handleSwitchingButtons(e,true));
	prevbtn.addEventListener('click',(e)=> handleSwitchingButtons(e,false));
	calview.addEventListener('click',handleCalendarCellClick);
	calscheme.addEventListener('click',handleCalendarSchemeClick);
	ordersendbtn.addEventListener('click',handleOrderSending);

	//ENDREGION

	setCurrentDayValues();
	insertTimeIntervalLabelsList(getIntervalLabelsList(chosentimelist));


}

document.addEventListener('DOMContentLoaded',run);