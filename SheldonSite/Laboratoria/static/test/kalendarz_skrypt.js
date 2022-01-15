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
	console.log("dzien tyg",firstWeekday);
	console.log("dzien ",firstDay);

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

function getSlug()
{
    const urlfragments = window.location.href.split('/');
    return urlfragments[urlfragments.length-1];
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

function getCookie(name)
    {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

function addZeroIfNeeded(number)
{
    if (number<=9) return "0"+number.toString();
    return number.toString();
}

function getSimpleDate(date)
{
const year = date.getUTCFullYear().toString();
const month = addZeroIfNeeded(date.getUTCMonth() + 1);
const day = addZeroIfNeeded(date.getDate());
return year+"-"+month+"-"+day;
}

function getDepartmentList()
{
 //TODO - It should get it from the server. Now examplary list:
 return ["Wydział górnictwa","Wydział automatyki elektroniki i informatyki","Komercyjny dostęp"];
}

function createDepartmentOption(value)
{
    const element = document.createElement('option');
    element.innerText = value;
    return element;
}

function createSelectDepartmentElement()
{
    const element = document.createElement('select');
    element.id = "order-department";
    const dataSource = getDepartmentList();
    dataSource.forEach((el)=>element.appendChild(createDepartmentOption(el)));
    return element;
}

function getOrderMessage()
{
    return document.getElementById('order-message').value.toString();
}

function getOrderDepartment()
{
    return document.getElementById('order-department').value.toString();
}

function getIntervals(intervalsList)
{
    const list = [];
    const dividedIntervalsList = getDividedIntervalsList(intervalsList);
	dividedIntervalsList.forEach((el)=>{
	    const obj = {}
	    obj.date = getSimpleDate(el[0].date);
	    const reservedIntervals = [];
	    el.forEach((x)=>{
	        reservedIntervals.push(x.time);
	    });
	    obj.intervals = reservedIntervals;
	    list.push(obj);
	});
	return list;
}

function getIntervalsShippingObject(intervalsList)
{
    const mainObj = {}
    mainObj.message = getOrderMessage();
	mainObj.list = getIntervals(intervalsList);
	mainObj.department = getOrderDepartment();
	mainObj.slug = getSlug();
	return JSON.stringify(mainObj);
}


function getDividedIntervalsList(intervalsList)
{
    intervalsList.sort(sortByDateAscending);
    let i = 0;
    const dividedIntervalsList = []
    while(i < intervalsList.length)
	{
		const intervalsListOfSingleDay = intervalsList.filter((el)=>{
			return el.date.getTime()==intervalsList[i].date.getTime();
		});
		dividedIntervalsList.push(intervalsListOfSingleDay);
		i+=intervalsListOfSingleDay.length;
	}
	return dividedIntervalsList;
}

function getIntervalLabelsList(intervalsList)
{
	const intervalsStringList = [];
	const dividedIntervalsList = getDividedIntervalsList(intervalsList);

	dividedIntervalsList.forEach((el)=>{
	    intervalsStringList.push(generateIntervalString(el));
	});
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
	if (userslist == null || userslist.length<=0) return '<span style="font-style:italic;">Wolne</span>';
	userslist.forEach((user)=>{
		aElementsList.push(`<a href=/account/${user}>${user}</a>&nbsp;`);
	});
	return aElementsList.join('');
}

function checkIfDatesSameDay(a,b)
{
    if (a.getDate()!=b.getDate()) return false;
    if (a.getMonth()!=b.getMonth()) return false;
    if (a.getFullYear()!=b.getFullYear()) return false;
    return true;
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

    let currentDay;
    setCurrentDayValues();

    generateCalendarCells(month_input.value,year_input.value);
    let calendarCells = document.querySelectorAll('.calendar-cell-active');
    markDayOnCalendar(currentDay.getDate());




	//INSERT DATA
    //let currentDay;
	//setCurrentDayValues();
    getRoomData()


	const chosentimelist = [];

	const calschemeCells = document.querySelectorAll('.scheme-row');
	calschemeCells[2].querySelector('.scheme-cell-content').insertAdjacentHTML('beforeend',getSchemeCellContent(["anna","maria","alek","gamon","fafefgwegw"]));
	calschemeCells[3].querySelector('.scheme-cell-content').insertAdjacentHTML('beforeend',getSchemeCellContent([]));
	//ENDREGION

	//REGION: Closures
	function handleMonthInput()
	{
		generateCalendarCells(month_input.value,year_input.value);
		markDayOnCalendarIfNeeded();
		//calendarCells = document.querySelectorAll('.calendar-cell-active');
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
		markDayOnCalendarIfNeeded();
		//calendarCells = document.querySelectorAll('.calendar-cell-active');
	}

	function handleCalendarCellClick(e)
	{
		if (e.target.classList.contains('calendar-cell-active'))
		{
			currentDay = new Date(year_input.value,month_input.value,Number(e.target.innerText));
            updateRoomData(roomData);
            setChosenSchemeCells();
			dayheader.innerText = getDayString(currentDay);
			[...document.getElementsByClassName('calendar-cell-current')].forEach((el)=>{
				el.classList.remove('calendar-cell-current');
			});
			e.target.classList.add('calendar-cell-current');
		}
	}

	function setSchemeRowChosen(row)
	{
	    row.className = 'scheme-row scheme-row-chosen';
	}

	function setSchemeRowNotChosen(row)
	{
        row.className = 'scheme-row';
	}

	function handleCalendarSchemeClick(e)
	{
		if (e.target.classList.contains('scheme-cell-choosebtn'))
		{
			const el = e.target.parentNode;
			const timeobj = {date:currentDay,time:Number(el.getAttribute('value'))};
			console.log("timeojb",timeobj);
			const res = indexOfList(chosentimelist,timeobj);
			if (res>-1)
			{
				chosentimelist.splice(res,1);
				//el.classList.remove('scheme-row-chosen');
				setSchemeRowNotChosen(el);
			}
			else
			{
				chosentimelist.push(timeobj);
				//el.classList.add('scheme-row-chosen');
				setSchemeRowChosen(el);
			}
			insertTimeIntervalLabelsList(getIntervalLabelsList(chosentimelist));
			//console.log(getDividedIntervalsList(chosentimelist));
			console.log(chosentimelist);
			console.log(getIntervals(chosentimelist));
			console.log(JSON.parse(getIntervalsShippingObject(chosentimelist)));
		}
	}
    /*
	function getCSRFToken()
    {
      if (!document.cookie) return null;
      const arr = document.cookie.split(';').map((c)=>{return c.split('=')}).map((c)=>{return c.trim()).flat();
      return arr[arr.indexOf("csrftoken")+1];
    }
    */

	function handleOrderSending(e)
	{
		e.preventDefault();
		if (confirm(getOrderAlertText(getIntervalLabelsList(chosentimelist),orderMessageArea.value)))
		{
			console.log("wszedlem do funkcji, gdzie generuje sie request post (fetch)");
			const data = getIntervalsShippingObject(chosentimelist);
			data.slug = getSlug();
			console.log(data);
			const csrftoken = getCookie('csrftoken');
            const headers = new Headers();
            headers.append('X-CSRFToken', csrftoken);
            //alert(document.querySelector('[name=csrfmiddlewaretoken]').value);
			fetch("test", {
			  method: 'POST',
              body: data,
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

	let roomData;

	function parseRoomData(data)
	{

	}

	function getSchemeContentType(type)
	{
	    let classname = "scheme-cell scheme-cell-content";
	    if (type=='red' || type=='green' || type=='orange')
	    {
	        return classname+' scheme-cell-'+type;
	    }
	    return classname;
	}

	function getCurrentDayObject(data)
	{
	    let element = null;
	    data.forEach((el)=>{
	        const date = new Date(el.fields.registerDate);
	        if (checkIfDatesSameDay(date,currentDay))
	        {
	            element = el;
	            return;
	        }
	    });
	    return element;
	}

	function setDefaultScheme()
	{
	    const scheme = document.getElementById('calendar-day-scheme');
	    const rows = document.getElementsByClassName('scheme-row');
	    [...rows].forEach((x)=>{
	        const content = x.querySelector('.scheme-cell-content');
	        content.className = getSchemeContentType('green');
	        content.innerHTML = "";
	        content.insertAdjacentHTML('beforeend', getSchemeCellContent([]));
	    });
	}

	function getRegisteredPeopleArray(data,id)
	{
	    if (!Number.isInteger(id)) return [];
	    if (id<0 || id>23) return [];
	    idString = parseInt(id).toString();
	    return data.fields['res_name_'+idString];
	}

	function updateRoomData(data)
	{
        const currentDayData = getCurrentDayObject(data);
        setDefaultScheme();
        if (currentDayData == null) return;
        const schemeRows = [...document.getElementsByClassName('scheme-row')];
        const reserved = currentDayData.fields.reserved.split(',');
        if (reserved[0]=="") return;
        reserved.forEach((i)=>{
            const interval = parseInt(i);
            const content = schemeRows[interval].querySelector('.scheme-cell-content');
            content.className = getSchemeContentType('red');
            content.innerHTML = "";
	        content.insertAdjacentHTML('beforeend', getSchemeCellContent(getRegisteredPeopleArray(currentDayData,interval)));
        });
        const pending = currentDayData.fields.pending.split(',');
        if (pending[0]=="") return;
        pending.forEach((i)=>{
            const interval = parseInt(i);
            const content = schemeRows[interval].querySelector('.scheme-cell-content');
            content.className = getSchemeContentType('orange');
            //TODO: handling pending usernames
            //TODO: orange intervals different on conflicts (stripes)
            content.innerHTML = "";
        });
	}

	function getRoomData()
	{
        const data = { username: 'example' };
			const csrftoken = getCookie('csrftoken');
            const headers = new Headers();
            const obj = { a: 'b' };
            headers.append('X-CSRFToken', csrftoken);
            //alert(document.querySelector('[name=csrfmiddlewaretoken]').value);
			fetch("api/"+getSlug(), {
			  method: 'GET',
              mode: 'same-origin',
			  headers: headers,
			  credentials: 'include'
			})
			.then(response => response.json())
			.then(data => {
			  console.log('Success:', data);
			  const obj = JSON.parse(data);
			  console.log(obj);
			  roomData = obj;
			  updateRoomData(roomData);
			  alert("Uzyskano dane.");
			})
			.catch((error) => {
			  console.error('Error:', error);
			});
	}

	function setCurrentDayValues()
	{
		const now = new Date();
		console.log('now',now);
		month_input.value = now.getMonth();
		year_input.value = now.getFullYear();

		currentDay = new Date(now.getFullYear(),now.getMonth(),now.getDate());
		dayheader.innerText = getDayString(currentDay);
		//[...document.querySelectorAll('.calendar-cell-active')][currentDay.getDate()-1].classList.add('calendar-cell-current');
		//calendarCells[currentDay.getDate()-1].classList.add('calendar-cell-current');
	}

    function clearCalendarCells()
    {
        const activecells = [...document.querySelectorAll('.calendar-cell')];
        activecells.forEach((el)=>{
            el.classList.remove('calendar-cell-current');
        });
    }

	function markDayOnCalendar(day)
	{
	    const activecells = [...document.querySelectorAll('.calendar-cell-active')];
	    if (activecells==null || activecells.length<28)
	        {
	            console.log("error with calendar cells",activecells);
	            return;
	        }
	    try{
	        clearCalendarCells();
            dayId = day-1;
            for (let i = 0 ; i < activecells.length ; i++)
                {
                    if (i==dayId)
                    {
                        console.log(day);
                        activecells[i].classList.add('calendar-cell-current');
                        break;
                    }
                }
            }
	    catch{
            console.log("day out of bounds.");
            return;
	    }
	}

	function markDayOnCalendarIfNeeded()
	{
	    if (currentDay.getMonth() == month_input.value && currentDay.getFullYear() == year_input.value)
	    {
	        markDayOnCalendar(currentDay.getDate());
	        return;
	    }
	    clearCalendarCells();
	    return;
	}

	function setChosenSchemeCells()
    {
        const intervals = getIntervals(chosentimelist);
        const current = intervals.filter((el)=>{
            const result = checkIfDatesSameDay(new Date(el.date),currentDay);
            console.log(result);
			return result;
		});
		        //console.log(intervals,current);
		//if (current.length>0) console.log(current);
		const schemeRows = [...document.getElementsByClassName('scheme-row')];
		schemeRows.forEach((el)=>
		{
		    setSchemeRowNotChosen(el);
		});
		if (current==null || current==undefined || current.length<=0) return;
		console.log(current);
		current[0].intervals.forEach((i)=>{
		    setSchemeRowChosen(schemeRows[i]);
		});
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


	insertTimeIntervalLabelsList(getIntervalLabelsList(chosentimelist));

    document.getElementById('order-department-section').appendChild(createSelectDepartmentElement());


}

document.addEventListener('DOMContentLoaded',run);