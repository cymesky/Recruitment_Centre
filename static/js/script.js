const filterField = document.querySelector('.filter-field')
const lvlField = document.querySelector('.lvl-field')
const tableAllSkillsBody = document.querySelector('.all-skills-body')
const tableNeededSkillsBody = document.querySelector('.needed-skills-body')
const btnAdd = document.querySelector('.add-button')
const btnRemove = document.querySelector('.btn-remove')
const btnFindPilot = document.querySelector('.btn-find-pilot')
const btnBack = document.querySelector('.btn-back')
const tablePilotsPlace = document.querySelector('.table-pilots-place')
const tablesPlace1 = document.querySelector('.tables-place1')
const tablesPlace2 = document.querySelector('.tables-place2')
const tablePilotsBody = document.querySelector('.table-pilots-body')
const rowFindPilotBtn = document.querySelector('.row-find')
const rowBackBtn = document.querySelector('.row-back')

const URL = 'http://127.0.0.1:8000/api/AllSkills/'
let URLSearchPilots = 'http://127.0.0.1:8000/api/Search/?'

// All available in game skills
const skills = []

// FUNCS
loadElementsToTable = () => {
  skills.forEach((skillName) => {
    // Prepare cell
    const tr = document.createElement('tr')
    const td = document.createElement('td')
    const td_text = document.createTextNode(skillName)

    // Add cell to table
    td.append(td_text)
    tr.append(td)
    tableAllSkillsBody.append(tr)
  })
}

getResults = (input) => {
  const results = []
  for (i = 0; i < skills.length; i++) {
    if (
      input.toLowerCase() === skills[i].slice(0, input.length).toLowerCase()
    ) {
      results.push(skills[i])
    }
  }
  return results
}

togglerBtns = () => {
  btnRemove.classList.toggle('btn-secondary')
  btnRemove.classList.toggle('btn-danger')
  if (btnRemove.disabled) {
    btnRemove.disabled = false
  } else {
    btnRemove.disabled = true
  }

  if (btnAdd.disabled) {
    btnAdd.disabled = false
  } else {
    btnAdd.disabled = true
  }

  if (lvlField.disabled) {
    lvlField.disabled = false
  } else {
    lvlField.disabled = true
  }
}

refreshSite = () => {
  btnRemove.disabled = true
  btnRemove.classList.remove('btn-danger')
  btnRemove.classList.add('btn-secondary')

  btnAdd.disabled = true

  lvlField.disabled = true
  lvlField.value = ''
  lvlField.setAttribute('placeholder', '')
  lvlField.classList.remove('border', 'border-danger')

  filterField.disabled = false
  filterField.value = ''

  btnFindPilot.disabled = true
}

clearPilotsTable = () => {
  if (tablePilotsBody.rows.length > 0) {
    Array.from(tablePilotsBody.rows).forEach((i) => i.remove())
  }
}

addToTablePilotsFromApi = (url) => {
  fetch(url)
    .then((response) => response.json())
    .then((jsonresponse) => {
      const pilots = jsonresponse
      // if we have pilots from api then add them to pilots table
      if (pilots.length > 0) {
        pilots.forEach((pilot) => {
          // prepare fields from api
          pilotToonUrl = pilot.post_toon_url.replace('api.', '')

          // create elements
          const tr = document.createElement('tr')

          const tdName = document.createElement('td')
          const name = document.createTextNode(pilot.name)
          tdName.append(name)

          const tdSkillpoints = document.createElement('td')
          const skillpoints = document.createTextNode(pilot.total_sp)
          tdSkillpoints.append(skillpoints)

          const tdPost = document.createElement('td')
          const aPost = document.createElement('a')
          aPost.setAttribute('href', pilot.post_url)
          aPost.setAttribute('target', '_blank')
          const spanPost = document.createElement('span')
          spanPost.classList.add('badge', 'rounded-pill', 'text-bg-secondary')
          spanPost.innerHTML = 'GO TO POST'
          aPost.append(spanPost)
          tdPost.append(aPost)

          const tdProfile = document.createElement('td')
          const aProfile = document.createElement('a')
          aProfile.setAttribute('href', pilotToonUrl)
          aProfile.setAttribute('target', '_blank')
          const spanProfile = document.createElement('span')
          spanProfile.classList.add(
            'badge',
            'rounded-pill',
            'text-bg-secondary',
          )
          spanProfile.innerHTML = 'GO TO PROFILE'
          aProfile.append(spanProfile)
          tdProfile.append(aProfile)

          tr.append(tdName, tdSkillpoints, tdPost, tdProfile)
          tablePilotsBody.append(tr)
        })
      }
    })
}

// EVENTS

// When website load
window.onload = function () {
  // Get data from api
  fetch(URL)
    .then((response) => response.json())
    .then((jsonresponse) => {
      jsonresponse.forEach((item) => skills.push(item['skill_name']))
      refreshSite()
      // Load elements from api to table
      loadElementsToTable()
      // clear all fields
    })
}

// When type in filter input field
filterField.oninput = function () {
  let results = []
  const userInput = this.value

  tableAllSkillsBody.innerHTML = ''
  if (userInput.length > 0) {
    results = getResults(userInput)
    for (i = 0; i < results.length; i++) {
      // prepare cell
      const tr = document.createElement('tr')
      const td = document.createElement('td')
      const td_text = document.createTextNode(results[i])

      // add cell to all skills table
      td.append(td_text)
      tr.append(td)
      tableAllSkillsBody.append(tr)
    }
  } else {
    loadElementsToTable()
  }
}

// When click on item in all skills table
tableAllSkillsBody.onclick = function (event) {
  if (tableAllSkillsBody.rows.length > 0) {
    const setValue = event.target.innerText
    filterField.value = setValue
    tableAllSkillsBody.innerHTML = ''
    filterField.disabled = true
    togglerBtns()
    lvlField.setAttribute('placeholder', 'set lvl 1-5')
    lvlField.focus()
  }
}

btnRemove.onclick = () => {
  filterField.value = ''
  lvlField.value = ''
  lvlField.disabled = true
  filterField.disabled = false
  togglerBtns()

  loadElementsToTable()
  refreshSite()
}

btnAdd.onclick = () => {
  const lvlNum = lvlField.value
  if (filterField !== '' && !isNaN(lvlNum) && lvlNum > 0 && lvlNum <= 5) {
    // create cells
    const tr = document.createElement('tr')
    const td1 = document.createElement('td')
    const td2 = document.createElement('td')
    const td3 = document.createElement('td')
    const td1_text = document.createTextNode(filterField.value)
    const td2_text = document.createTextNode(lvlNum)
    const td3_btn = document.createElement('button')

    // styling cells
    td1.classList.add('w-50')
    td2.classList.add('w-25')
    td3.classList.add('w-25')
    td3_btn.classList.add('btn', 'btn-danger', 'btn-remove-item')
    td3_btn.innerHTML = '<i class="fas fa-thin fa-delete-left"></i>'

    // add cells to needed skills table
    td1.append(td1_text)
    td2.append(td2_text)
    td3.append(td3_btn)
    tr.append(td1, td2, td3)
    tableNeededSkillsBody.append(tr)

    // remove skill from skills list
    const indexOfSkill = skills.indexOf(filterField.value)
    skills.splice(indexOfSkill, 1)

    refreshSite()
    loadElementsToTable()

    // enable or disable find pilot button
    tableNeededSkillsBody.rows.length > 0
      ? (btnFindPilot.disabled = false)
      : (btnFindPilot.disabled = true)
  } else {
    lvlField.classList.add('border', 'border-danger')
    lvlField.value = ''
  }
}

// When click remove btn on needed skills table
tableNeededSkillsBody.onclick = (event) => {
  if (event.target.tagName === 'I' || event.target.tagName === 'BUTTON') {
    const tr = event.target.closest('tr')
    skills.push(tr.firstChild.textContent)
    tr.remove()
    // enable or disable find pilot button
    tableNeededSkillsBody.rows.length > 0
      ? (btnFindPilot.disabled = false)
      : (btnFindPilot.disabled = true)
  }
}

btnFindPilot.onclick = () => {
  // clear pilots table
  clearPilotsTable()
  // Hide tables with skills and show table with pilots
  tablesPlace1.classList.add('hide')
  tablesPlace2.classList.add('hide')
  setTimeout(() => {
    tablesPlace1.classList.add('d-none')
    tablesPlace2.classList.add('d-none')
    tablePilotsPlace.classList.remove('d-none', 'hide')
  }, 2000)
  // Change buttons from find to back to browser
  rowBackBtn.classList.remove('d-none')
  rowFindPilotBtn.classList.add('d-none')

  rowBackBtn.classList.add('change')
  // Turn off filter field
  filterField.disabled = true
  filterField.placeholder = ''

  // Getting needed skills name and lvl
  const neededSkills = {}

  for (const skill of tableNeededSkillsBody.rows) {
    let skillName = skill.children[0].textContent
    skillName = skillName.replaceAll(' ', '+')
    neededSkills[skillName] = skill.children[1].textContent
  }

  // Create slug for api search
  let slug = ''

  if (Object.keys(neededSkills).length > 0) {
    for (const skill in neededSkills) {
      slug += `${skill}=${neededSkills[skill]}&`
    }

    slug = slug.slice(0, -1)

    const requestURL = URLSearchPilots + slug
    // Fetch from api data and add to pilots table
    addToTablePilotsFromApi(requestURL)
  }
}
btnBack.onclick = () => {
  // Hide pilots table and show browser tables
  tablePilotsPlace.classList.add('hide')
  setTimeout(() => {
    tablePilotsPlace.classList.add('d-none')
    tablesPlace1.classList.remove('hide', 'd-none')
    tablesPlace2.classList.remove('hide', 'd-none')
  }, 2000)
  // Change buttons from back to find
  rowBackBtn.classList.add('d-none')
  rowFindPilotBtn.classList.remove('d-none')

  // enable or disable find pilot button
  tableNeededSkillsBody.rows.length > 0
    ? (btnFindPilot.disabled = false)
    : (btnFindPilot.disabled = true)

  filterField.disabled = false
}
