;
; Macro to dial a standard local extension
;
; format: Macro(stdexten,dest,context,voicebox 1/0)
;
[macro-dial-std-exten]
;
; test for CFIM (Call Forwarding Immediate)
exten=s,1,DBget(temp=CFIM/${MACRO_EXTEN})
exten=s,2,Goto(${ARG2},${temp})

; no CFIM
exten=s,102,DBGet(temp=DND/${MACRO_EXTEN})
; no CFIM, DND set
exten=s,103,GotoIf($[${ARG3}vm = 1vm]?105:104)
; no CFIM, DND set, but no voicemaiL:
;TODO: set cause code
exten=s,104,Hangup
; no CFIM, DND set, voicemail set:
exten=s,105,Macro(voicemail,u${MACRO_EXTEN})
exten=s,106,Hangup

; no CFIM, no DND
exten=s,203,DBGet(dsec=DSEC/${MACRO_EXTEN})
exten=s,204,NoOp
exten=s,205,DBGet(dopt=DOPT/${MACRO_EXTEN})
exten=s,206,NoOp
exten=s,207,Dial(${ARG1},${dsec},${dopt})
; Dial result was 'timeout'
exten=s,208,SetVar(vmopt=u)
exten=s,209,Noop
exten=s,210,DBGet(temp=CFBS/${MACRO_EXTEN})
exten=s,211,Goto(${ARG2},${temp})

; no CFIM, no DND, no DSEC (dial seconds)
exten=s,304,SetVar(dsec=45)
exten=s,305,Goto(205)
; no CFIM, no DND, no DOPT (dial options)
exten=s,306,SetVar(dopt=Ttr)
exten=s,307,Goto(207)

; Dial result was 'unavailable' or 'busy'
exten=s,308,SetVar(vmopt=b)
exten=s,309,Noop
exten=s,310,Goto(210)

; dial did no go throught, CFBS not set
exten=s,311,GotoIf($[${ARG3}vm = 1vm]?313:312)
exten=s,312,Hangup
exten=s,313,Macro(voicemail,${vmopt}${MACRO_EXTEN})

exten=i,0,Hangup


;
; format: Macro(voicemail,<VoiceMail2 arguments>)
;
[macro-voicemail]
exten => s,1,Answer
exten => s,2,Wait(1)
exten => s,3,VoiceMail2(${ARG1})
;exten => s,104,Macro(dial-result,3)

;exten => h,1,Macro(dial-result)
;exten => t,1,Macro(dial-result)


;
; format: Macro(dial-result,[<cause>])
;
[macro-dial-result]
exten => s,1,AbsoluteTimeout(35)
exten => s,2,GotoIf($[foo${ARG1} != foo]?cause_${ARG1},1:cause_${HANGUPCAUSE},1)

; undefined error (mostly when an existing extension is currently unavailable)
exten => _cause_0,1,Answer
exten => _cause_0,2,Wait(1)
exten => _cause_0,3,Playback(the-number-u-dialed,skip)
exten => _cause_0,4,Playback(is-curntly-unavail,skip)
exten => _cause_0,5,Playback(pls-try-call-later,skip)
exten => _cause_0,6,Wait(3)
exten => _cause_0,7,Goto(3)

; normal call clearing
exten => _cause_1,1,Hangup

; extension currently busy
exten => _cause_2,1,Answer
exten => _cause_2,2,PlayTones(busy)
exten => _cause_2,3,Wait(40)
exten => _cause_2,4,Goto(2)

; something failed
exten => _cause_3,1,Answer
exten => _cause_3,2,PlayTones(info)
exten => _cause_3,3,Wait(2)
exten => _cause_3,4,Playback(an-error-has-occured,skip)
exten => _cause_3,5,Playback(pls-try-call-later,skip)
exten => _cause_3,6,Wait(2)
exten => _cause_3,7,Goto(2)

; congestion
exten => _cause_4,2,Congestion

; unassigned number
exten => _cause_5,1,Answer
exten => _cause_5,2,PlayTones(info)
exten => _cause_5,3,Wait(2)
exten => _cause_5,4,Playback(ss-noservice,skip)
exten => _cause_5,5,Wait(2)
exten => _cause_5,6,Goto(2)

; unallowed number
exten => _cause_99,1,Answer
exten => _cause_99,2,PlayTones(info)
exten => _cause_99,3,Wait(2)
exten => _cause_99,4,Playback(discon-or-out-of-service,skip)
exten => _cause_99,5,Wait(2)
exten => _cause_99,6,Goto(2)

; unauthorized extension
exten => _cause_100,1,Answer
exten => _cause_100,2,PlayTones(info)
exten => _cause_100,3,Wait(2)
exten => _cause_100,6,Playback(your-extension,skip)
exten => _cause_100,7,Playback(not-yet-assigned,skip)
exten => _cause_100,8,Playback(please-contact-tech-supt,skip)
exten => _cause_100,9,Wait(2)
exten => _cause_100,10,Goto(2)

; all other errors
exten => _cause_X.,1,Answer
exten => _cause_X.,2,PlayTones(info)
exten => _cause_X.,3,Wait(2)
exten => _cause_X.,4,Playback(an-error-has-occured,skip)
exten => _cause_X.,5,Playback(error-number,skip)
exten => _cause_X.,6,GotoIf($[foo${ARG1} != foo]?7:11)
exten => _cause_X.,7,Say_Number(${ARG1})
exten => _cause_X.,8,Wait(1)
exten => _cause_X.,9,Playback(please-contact-tech-supt,skip)
exten => _cause_X.,10,Goto(14)
exten => _cause_X.,11,SayNumber(${HANGUPCAUSE})
exten => _cause_X.,12,Wait(1)
exten => _cause_X.,13,Playback(please-contact-tech-supt,skip)
exten => _cause_X.,14,Wait(2)
exten => _cause_X.,15,Goto(2)

exten => T,1,PlayTones(congestion)
exten => T,2,Wait(5)
exten => T,3,Hangup


