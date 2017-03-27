; Assignment: Snake Game
; Team Name: Team Heartburn
; Students: Connor Duignan (13392886), Thomas Reaney (13436018), Cian Duffy (13399326)

; ===================== Main Program ======================
; FUNCTION: Used to set up the timer, game boundary, snake and food
; Set R0 to 0FFFh (the end of data memory)
XOR R0, R0, R0						; Clear R0
INV R0, R0							; R0: 1111 1111 1111 1111 (FFFFh)						
SHRL R0, 4							; R0: 0000 1111 1111 1111 (0FFFh)
XOR R1, R1, R1						; Clear R1
MOVBAMEM @R1, R1					; Clear address 0

ClearMemoryLoop:					; Loop down through data memory and clear every address using R1
MOVBAMEM @R0, R1
DEC R0, R0
JNZ R0, ClearMemoryLoop				; If the start of memory has not been reached, continue looping

CALL MakeSeed						; Make a seed for the random number generator
CALL TimerSetup						; Set up the interrupt timer
CALL SnakeSetup						; Set up the initial snake position
CALL GenerateFood					; Generate initial food position
CALL TimerEnable					; Enable the timer and interrupts
END		    						; End Main Program
; =========================================================


; ============== Interrupt Service Routine 2 ==============
ISR2: ORG 116
CALL CheckButtons					; Figures out which direction the snake should move in
CALL MoveSnakeHead					; Updates the position and direction of the snakes head

XOR R0, R0, R0						; Clear R0
SETBR R0, 8							; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R6, @R0					; Get register from address R0 and store it in R6

; DEBUG
SHRL R0, 4							; Clear first 4 bits in R0
DEC R0, R0							; Decrement R0
MOVBAMEM @R0, R6					; Move R6 into address R0 in data memory
;  +++++++

CALL DisplayOnWidget				; Display the snake on the colour widget

CALL GetXPosition					; Get the x-position of the snake
MOVRR R6, R7						; Move R7 into R6
CALL FourToSixteenDecoder			; Decode x-position of the snake
MOVRR R0, R7						; Move R7 into R0

CALL GetYPosition					; Get y-position of the snake
MOVRR R1, R7						; Move R7 into R1
XOR R2, R2, R2						; Clear R2
SETBR R2, 4							; R2: 0000 0000 0001 0000 (0010h)
ADD R1, R2, R1						; Add R2 and R1 and store the result in R1

MOVAMEMR R2, @R1					; Get register from address R1 in data memory and store the result in R2
OR R2, R2, R0						; OR R2 with R0 and store the result in R2
MOVBAMEM @R1, R2					; Move R2 to address R1 in data memory
RETI        						; Return from interrupt
; =========================================================


; ======================= MakeSeed ========================
; FUNCTION: Used to make a seed for the random number generator
MakeSeed:
XOR R0, R0, R0                      ; Clear R0
SETBR R0, 3                         ; R0: 0000 0000 0000 1000 (0008h)
SETBR R0, 0                         ; R0: 0000 0000 0000 1001 (0009h)
SETBR R0, 4                         ; R0: 0000 0000 0001 1001 (0019h)
SETBR R0, 7                         ; R0: 0000 0000 1001 1001 (0099h)
SETBR R0, 10                        ; R0: 0000 0100 1001 1001 (0499h)
SETBR R0, 13                        ; R0: 0010 0100 1001 1001 (2499h)
; Store the seed in BRAM at address 253d
XOR R1, R1, R1						; Clear R1
SETBR R1, 8							; R1: 0000 0001 0000 0000 (0100h)
DEC R1, R1							; R1: 0000 0000 1111 1111 (00FFh)
DEC R1, R1							; R1: 0000 0000 1111 1110 (00FEh)
DEC R1, R1							; R1: 0000 0000 1111 1101 (00FDh)

MOVBAMEM @R1, R0					; Move R0 into address R1 in data memory
RET									; Return from subroutine
; =========================================================


; ================ RandomNumberGenerator ==================
; FUNCTION: Used to generate a random number based on a seed
RandomNumberGenerator:
; Get address of seed
XOR R0, R0, R0						; Clear R0
SETBR R0, 8							; R0: 0000 0001 0000 0000 (0100h)
DEC R0, R0							; R0: 0000 0000 1111 1111 (00FFh)
DEC R0, R0							; R0: 0000 0000 1111 1110 (00FEh)
DEC R0, R0							; R0: 0000 0000 1111 1101 (00FDh)
; Get seed from data memory
MOVAMEMR R1, @R0                    ; Get register from address R0 and store it in R1
; Make new random number
ADD R2, R1, R1
DEC R2, R2
ADD R2, R1, R2
SUB R2, R1, R2
SUB R2, R1, R2
; Move new random number to the random number address
MOVBAMEM @R0, R2                    ; Move new random number in R2 to address 
MOVRR R1, R2                        ; Copy R2 into R1 so it can be reused 
; Get nibble for x-position
SHLL R1, 8
SHRL R1, 12
SHLL R1, 4
; Get nibble for y-position
SHLL R2, 12
SHRL R2, 12
; Combine the x-position and y-position
OR R7, R1, R2

RET                                 ; Return from subroutine
; =========================================================


; ===================== GenerateFood =========================
; FUNCTION: Used to set up the food
GenerateFood:
CALL RandomNumberGenerator			; Get random position of the food

MOVRR R1, R7						; Get the y-position
SHLL R1, 12
SHRL R1, 12

XOR R2, R2, R2						; Add an offset of 16d to the address
SETBR R2, 4
ADD R1, R2, R1

MOVRR R0, R7						; Get the x-position
SHLL R0, 8
SHRL R0, 12
MOVRR R6, R0						; Move R0 into R6
MOVRSFR SFR4, R6					; Move R6 into SFR4
CALL FourToSixteenDecoder
MOVRR R0, R7						; Move R7 into R0

MOVAMEMR R2, @R1					; Move the row the food will be in from memory
AND R2, R2, R0						; AND the food with the row taken from memory
JNZ R2, GenerateFood				; If the food will be in the same position as an existing object, generate a new food object

MOVAMEMR R2, @R1					; If the food is in a suitable position, display in BRAM
OR R2, R2, R0
MOVBAMEM @R1, R2

; Get the food vector address
XOR R7, R7, R7						; Clear R7
SETBR R7, 8							; R7: 0000 0001 0000 0000 (0100h)
DEC R7, R7							; R7: 0000 0000 1111 1111 (00FFh)
DEC R7, R7							; R7: 0000 0000 1111 1110 (00FEh)
DEC R7, R7							; R7: 0000 0000 1111 1101 (00FDh)

XOR R3, R3, R3						; Show the food vector in memory
SETBR R3, 3
MOVAMEMR R4, @R7
MOVBAMEM @R3, R4

XOR R6, R6, R6						; Set the colour of the food
SETBR R6, 1
CALL SetColour

XOR R3, R3, R3						; Show the food vector in memory
SETBR R3, 0
SETBR R3, 3
MOVAMEMR R4, @R7
MOVBAMEM @R3, R4

MOVAMEMR R6, @R7					; Display the food on the widget
CALL DisplayOnWidget				; Display snake on colour widget
RET									; Return from subroutine
; =========================================================


; ====================== DisplayOnWidget =======================
; FUNCTION: Used to display the snake on the colour widget
DisplayOnWidget:
MOVRR R0, R6
SHLL R0, 8                          ; Remove the other contents from R0 so that it only stores the x-position in the lowest nibble
SHRL R0, 12

MOVRR R1, R6
SHLL R1, 12                         ; Remove the other contents from R1 so that it only stores the y-position in the lowest nibble
SHRL R1, 12

MOVRR R2, R6
SHLL R2, 4							; Remove the other contents from R2 so that it only stores the colour in the lowest nibble
SHRL R2, 12

XOR R3, R3, R3						; Set R3 to 64d (40h)
SETBR R3, 6

XOR R4, R4, R4						; Set R4 to 4d (4h)
SETBR R4, 2

XOR R5, R5, R5						; Set R5 to Fh (a mask)
INV R5, R5
SHRL R5, 12

ConvertYPosition:
JZ R1, ConvertXPosition				; If R1 is 0, jump to ConvertXPosition
ADDI R3, R3, 4						; Increase R3 by 4
DEC R1, R1							; Decrement R1
XOR R6, R6, R6
JZ R6, ConvertYPosition				; Jump to ConvertYPosition

ConvertXPosition:
JZ R0, ShowColour					; If R0 is 0, jump to ShowColour
ROTL R5, 4							; Rotate the mask left by 4 bits
ROTL R2, 4							; Rotate the colour left by 4 bits
DEC R4, R4							; Decrement the counter
DEC R0, R0							; Decrement the x position
JNZ R4, ConvertXPosition			; If the counter is not 0, jump to ConvertXPosition
ADDI R4, R4, 4						; Reset R4 to 4h
INC R3, R3							; Increment R3
XOR R6, R6, R6
JZ R6, ConvertXPosition				; Jump to ConvertXPosition

ShowColour:
MOVAMEMR R4, @R3					; Get the row from memory
AND R5, R5, R4						; Mask the row
XOR R4, R5, R4						; Wipe the masked part of the row
OR R4, R4, R2						; Add the new colour to the row
MOVBAMEM @R3, R4

RET
; =========================================================


; ====================== TimerSetup =======================
; FUNCTION: Used to set up the 0.5 second timer
TimerSetup:
XOR R1, R1, R1						; Clear R1
SETBR R1, 15                		; R1: 1000 0000 0000 0000 (8000h)
SHRA R1, 7                 			; R1: 1111 1111 0000 0000 (FF00h)
SETBR R1, 6                 		; R1: 1111 1111 0100 0000 (FF40h)
SETBR R1, 0                 		; R1: 1111 1111 0100 0001 (FF41h)
MOVRR R0, R7                		; R0: 1111 1111 0100 0001 (FF41h)
ROTR R0, 8                 			; R0: 0100 0001 1111 1111 (41FFh)
SETBR R0, 9                 		; R0: 0100 0011 1111 1111 (43FFh)
CLRBR R0, 6                 		; R0: 0100 0011 1101 1111 (43DFh)
MOVRSFR SFR1, R0					; Set TMRL to R0
MOVRSFR SFR6, R0					; Set TMRL_LDVAL to R0
MOVRSFR SFR2, R1					; Set TMRH to R1
MOVRSFR SFR7, R1					; Set TMRH_LDVAL to R1
RET									; Return from subroutine
; =========================================================


; ===================== SnakeSetup ========================
; FUNCTION: Used to set up the snake
SnakeSetup:
XOR R0, R0, R0      				; Clear R0
; Set the initial snake head vector
SETBR R0, 1							; R0: 0000 0000 0000 0010 (0002h)	
;SETBR R0, 7							; R0: 0000 0000 1000 0010 (0082h)
SETBR R0, 5
SETBR R0, 8							; R0: 0000 0001 1000 0010 (0182h)
;SETBR R0, 12						; R0: 0001 0001 0001 0010 (1112h)
SETBR R0, 13
; Set the snake head vector address
XOR R1, R1, R1      				; Clear R1
SETBR R1, 8     					; R1: 0000 0000 0100 0000 (0100h)
MOVBAMEM @R1, R0    				; Set up snake state vector

RET									; Return from subroutine
; =========================================================


; ====================== TimerEnable ======================
; FUNCTION: Used to enable the timer
TimerEnable:
XOR R0, R0, R0						; Clear R0
INV R0, R0							; R0: 1111 1111 1111 1111 (FFFFh)
SHLL R0, 13							; R0: 1110 0000 0000 0000 (E000h)
ROTL R0, 6							; R0: 0000 0000 0011 1000 (0038h)
SETBR R0, 0							; R0: 0000 0000 0011 1001 (0039h)
MOVRSFR SFR0, R0					; Move R0 into SFR0
RET									; Return from subroutine
; =========================================================


; ==================== CheckButtons =======================
; FUNCTION: Used to check the state of the buttons which determine the snake direction
CheckButtons:
CALL GetSnakeHeadDirection			; Get the direction of the snakes head
MOVRR R6, R7						; Store the direction in R6

MOVINL R0							; Read from inPort and store in R0

XOR R1, R1, R1						; Clear R1
SETBR R1, 0							; R1: 0000 0000 0000 0001 (0001h)
SUB R2, R1, R0						; Check if the snake should move clockwise
JZ R2, MovingClockwise				; If R2 is zero, jump to MovingClockwise

SHLL R1, 1							; R1: 0000 0000 0000 0010 (0002h)
SUB R2, R1, R0						; Check if the snake should move counter-clockwise
JZ R2, MovingCounterClockwise		; If R2 is zero, jump to MovingCounterClockwise
JNZ R2, ReturnFromCheckButtons		; If R2 is not zero, jump to ReturnFromCheckButtons

MovingClockwise:
XOR R6, R6, R6						; Clear R6

XOR R1, R1, R1						; Clear R1
SETBR R1, 0							; R1: 0000 0000 0000 0001 (0001h)
SUB R2, R1, R7						; If the snake's head is moving right, it should move down
JZ R2, SetSnakeHeadDirDown			; If R2 is zero, jump to SetSnakeHeadDirDown

SHLL R1, 1							; R1: 0000 0000 0000 0010 (0002h)
SUB R2, R1, R7						; If the snake's head is moving left, it should move up
JZ R2, SetSnakeHeadDirUp			; If R2 is zero, jump to SetSnakeHeadDirUp

SHLL R1, 1							; R1: 0000 0000 0000 0100 (0004h)
SUB R2, R1, R7						; If the snake's head is moving up, it should move down
JZ R2, SetSnakeHeadDirRight			; If R2 is zero, jump to SetSnakeHeadDirRight

SHLL R1, 1							; R1: 0000 0000 0000 1000 (0008h)
SUB R2, R1, R7						; If the snake's head is moving down, it should move left
JZ R2, SetSnakeHeadDirLeft			; If R2 is zero, jump to SetSnakeHeadDirLeft

MovingCounterClockwise:
XOR R6, R6, R6						; Clear R6

XOR R1, R1, R1						; Clear R1
SETBR R1, 0							; R1: 0000 0000 0000 0001 (0001h)
SUB R2, R1, R7						; If the snake's head is moving right, it should move up
JZ R2, SetSnakeHeadDirUp			; If R2 is zero, jump to SetSnakeHeadDirUp

SHLL R1, 1							; R1: 0000 0000 0000 0010 (0002h)
SUB R2, R1, R7						; If the snake's head is moving left, it should move down
JZ R2, SetSnakeHeadDirDown			; If R2 is zero, jump to SetSnakeHeadDirDown

SHLL R1, 1							; R1: 0000 0000 0000 0100 (0004h)
SUB R2, R1, R7						; If the snake's head is moving up, it should move left
JZ R2, SetSnakeHeadDirLeft			; If R2 is zero, jump to SetSnakeHeadDirLeft

SHLL R1, 1							; R1: 0000 0000 0000 1000 (0008h)
SUB R2, R1, R7						; If the snake's head is moving down, it should move right
JZ R2, SetSnakeHeadDirRight			; If R2 is zero, jump to SetSnakeHeadDirRight

SetSnakeHeadDirDown:
SETBR R6, 3							; Set the snake's direction to down
JNZ R6, ReturnFromCheckButtons		; If R6 is not zero, jump to ReturnFromCheckButtons

SetSnakeHeadDirUp:
SETBR R6, 2							; Set the snake's direction to up
JNZ R6, ReturnFromCheckButtons		; If R6 is not zero, jump to ReturnFromCheckButtons

SetSnakeHeadDirLeft:
SETBR R6, 1							; Set the snake's direction to left
JNZ R6, ReturnFromCheckButtons		; If R6 is not zero, jump to ReturnFromCheckButtons

SetSnakeHeadDirRight:
SETBR R6, 0							; Set the snake's direction to right

ReturnFromCheckButtons:
CALL SetSnakeHeadDirection			; Set new direction of the snake
RET                            		; Return from subroutine
; =========================================================


; =================== MoveSnakeHead =======================
; FUNCTION: Used to move the snake's head
MoveSnakeHead:
CALL GetSnakeHeadDirection			; Get the direction of the snake's head
MOVRR R3, R7
XOR R0, R0, R0						; Clear R0
SETBR R0, 0							; R0: 0000 0000 0000 0001 (0001h)
SUB R1, R7, R0						; If the snake's direction is right, move it right
JZ R1, CallMoveRight				; If R1 is zero, jump to CallMoveRight

SHLL R0, 1							; R0: 0000 0000 0000 0010 (0002h)
SUB R1, R7, R0						; If the snake's direction is left, move it left
JZ R1, CallMoveLeft					; If R1 is zero, jump to CallMoveLeft

SHLL R0, 1							; R0: 0000 0000 0000 0100 (0004h)
SUB R1, R7, R0						; If the snake's direction is up, move it up
JZ R1, CallMoveUp					; If R1 is zero, jump to CallMoveUp

SHLL R0, 1							; R0: 0000 0000 0000 1000 (0008h)
SUB R1, R7, R0						; If the snake's direction is down, move it down
JZ R1, CallMoveDown					; If R1 is zero, jump to CallMoveDown

CallMoveRight:
CALL MoveSnakeHeadRight				; Move the snake's head right
RET									; Return from subroutine

CallMoveLeft:
CALL MoveSnakeHeadLeft				; Move the snake's head left
RET									; Return from subroutine

CallMoveUp:
CALL MoveSnakeHeadUp				; Move the snake's head up
RET									; Return from subroutine

CallMoveDown:
CALL MoveSnakeHeadDown				; Move the snake's head down
RET									; Return from subroutine
; =========================================================


; ================= FourToSixteenDecoder ==================
; FUNCTION: Used as a 4-to-16 decoder
FourToSixteenDecoder:
XOR R7, R7, R7                      ; Clear R7
SETBR R7, 0                         ; R7: 0000 0000 0000 0001 (0001h)

DecoderLoop:
JZ R6, ReturnFromDecoder            ; If R6 is 0000h, jump to ReturnFromDecoder
SHLL R7, 1                          ; Shift the set bit in R7 left by 1
DEC R6, R6                          ; Decrement R6
JNZ R6, DecoderLoop                 ; If R6 is not 0000h, jump to DecoderLoop

ReturnFromDecoder:
RET                                 ; Return from subroutine
; =========================================================


; ==================== GetXPosition =======================
; FUNCTION: Used to get the x-position of the snake's head or tail (determined by address in R6)
GetXPosition:
XOR R7, R7, R7						; Clear R0
SETBR R7, 8							; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R7, @R7                    ; Get the snake head vector and store in R7
SHLL R7, 8                          ; Remove the other contents from R7 so that it only stores the x position in the lowest nibble
SHRL R7, 12
RET                                 ; Return from subroutine
; =========================================================


; ==================== GetYPosition =======================
; FUNCTION: Used to get the y-position of the snake's head
GetYPosition:
XOR R7, R7, R7						; Clear R0
SETBR R7, 8							; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R7, @R7                    ; Get the snake head vector and store in R7
SHLL R7, 12                         ; Remove the other contents from R7 so that it only stores the y co-ordinate in the lowest nibble
SHRL R7, 12
RET                                 ; Return from subroutine
; =========================================================


; ================ GetSnakeHeadDirection ==================
; FUNCTION: Used to get the direction of the snake's head
GetSnakeHeadDirection:
XOR R7, R7, R7                		; Clear R7
SETBR R7, 8                    		; Set R7 to 0100h, the address of the snake head vector
MOVAMEMR R7, @R7            		; Get the vector from the address in R7 and store in R7
SHRL R7, 12                    		; Remove the other contents from R7 so that it only stores the direction in the lowest nibble
RET                            		; Return from subroutine
; =========================================================


; ================ SetSnakeHeadDirection ==================
; FUNCTION: Used to set the direction of the snake's head
SetSnakeHeadDirection:
XOR R0, R0, R0                		; Clear R0
; Set the address of the snake head vector
SETBR R0, 8                    		; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R1, @R0            		; Get the vector from the address in R0 and store in R0
SHLL R1, 4                    		; Rotate R0 left by 4 to clear the direction
OR R1, R1, R6                		; OR R6 with R0 to combine the input with the snake head vector
ROTR R1, 4                    		; Rotate the vector so the direction is in the highest nibble
MOVBAMEM @R0, R1
RET                            		; Return from subroutine
; =========================================================


; ================ GetColour ==================
; FUNCTION: Used to the get the colour of the vector from the address in R6
GetColour:
MOVAMEMR R7, @R6            		; Get the vector from the address in R6 and store in R7
SHLL R7, 4							; Remove the other contents from R7 so that it only stores the colour in the lowest nibble
SHRL R7, 12                    		
RET                            		; Return from subroutine
; =============================================


; ================ SetColour ==================
; FUNCTION: Used to the set the colour of the vector in R7
SetColour:
MOVAMEMR R1, @R7            		; Get the vector from the address in R7 and store in R1
ROTR R1, 8
SHRL R1, 4
SHLL R1, 4
OR R1, R1, R6
ROTL R1, 8
MOVBAMEM @R7, R1          		
RET                            		; Return from subroutine
; =============================================


; ================== MoveSnakeHeadLeft ====================
; FUNCTION: Used to move the snake's head left by incrementing the x-position of the snake's head
MoveSnakeHeadLeft:
XOR R0, R0, R0                      ; Clear R0
SETBR R0, 8                         ; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R1, @R0                    ; Get the head state vector from memory and store in R1
ROTR R1, 4                          ; Rotate R1 right by 4 to move the snake's head x co-ordinate to the lowest nibble
INC R1, R1                          ; Increment the x-position
ROTL R1, 4                          ; Rotate R1 back
MOVBAMEM @R0, R1                    ; Move the updated snake head vector back to memory
RET                                 ; Return from subroutine
; =========================================================


; ================== MoveSnakeHeadRight ===================
; FUNCTION: Used to move the snake's head right by decrementing the x-position of the snake's head
MoveSnakeHeadRight:
XOR R0, R0, R0                      ; Clear R0
SETBR R0, 8                         ; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R1, @R0                    ; Get the snake head vector from memory and store in R1
ROTR R1, 4                          ; Rotate R1 right by 4 to move the snake's head x co-ordinate to the lowest nibble
DEC R1, R1                          ; Decrement the x-position
ROTL R1, 4                          ; Rotate R1 back
MOVBAMEM @R0, R1                    ; Move the updated snake head vector back to memory
RET                                 ; Return from subroutine
; =========================================================


; ================== MoveSnakeHeadUp ======================
; FUNCTION: Used to move the snake's head up by incrementing the y-position of the snake's head
MoveSnakeHeadUp:
XOR R0, R0, R0                      ; Clear R0
SETBR R0, 8                         ; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R1, @R0                    ; Get the snake head vector from memory and store in R1
INC R1, R1                          ; Increment the y-position
MOVBAMEM @R0, R1                    ; Move the updated snake head vector back to memory
RET                                 ; Return from subroutine
; =========================================================


; =================== MoveSnakeHeadDown ===================
; FUNCTION: Used to move the snake's head down by decrementing the y-position of the snake's head
MoveSnakeHeadDown:
XOR R0, R0, R0                      ; Clear R0
SETBR R0, 8                         ; R0: 0000 0001 0000 0000 (0100h)
MOVAMEMR R1, @R0                    ; Get the snake head vector from memory and store in R1
DEC R1, R1                          ; Decrement the y-position
MOVBAMEM @R0, R1                    ; Move the updated snake head vector back to memory
RET                                 ; Return from subroutine
; =========================================================


; =================== ShiftSnakeQueue ===================
; FUNCTION: Used to move the snake by shifting the snake positions
ShiftSnakeQueue:
XOR R5, R5, R5              		; Clear R5
SETBR R5, 8                 		; R5: 256d
DEC R5, R5                  		; R5: 255d
DEC R4, R5                  		; R5: 254d
MOVAMEMR R0, @R6            		; Initialise QueuePointer to TailPointer

ShiftQueueEntry:
DEC R1, R0                  		; Queue Pointer - 1d
MOVAMEMR R2, @R1            		; Move QueuePointer - 1d to R2
MOVBAMEM @R0, R2            		; Move R2 to QueuePointer
DEC R0, R0                  		; Decrement QueuePointer
SUB R3, R0, R5              		; R3 = QueuePointer - 255d
JNZ R3, ShiftQueueEntry     		; Repeat loop if R3 != 0d (i.e. if QueuePointer > 255d)

RET                         		; Return from function
; =======================================================


; =================== SetNextHeadPosition ===================
; FUNCTION: Used to set the next head position
SetNextHeadPosition:
XOR R0, R0, R0              		; Clear R5
SETBR R0, 8                			; R5: 256d
DEC R0, R0                  		; R5: 255d
MOVBAMEM @R0, R6            		; Move Next Head Position from R6 to address 255d in data memory
RET									; Return from subroutine
; ===========================================================


; =================== GetNextHeadPosition ===================
; FUNCTION: Used to get the next head position
GetNextHeadPosition:
XOR R0, R0, R0              		; Clear R5
SETBR R0, 8                 		; R5: 256d
DEC R0, R0                  		; R5: 255d
MOVAMEMR R7, @R0            		; Move Next Head Position from address 255d in memory to R7
RET									; Return from subroutine
; ===========================================================


; ==================== CheckBottomBoundary ==================
; FUNCTION: Used to check if the snake head is at the bottom boundary of the game
CheckBottomBoundary:
CALL GetYPosition					; Get y position of the snake
XOR R0, R0, R0						; Clear R0
SETBR R0, 4							; R0: 0000 0000 0001 0000 (0010h)
SUB R0, R0, R7						; Check if the snake is at the bottom boundary
JZ R0, CheckBottomRestartGame		; If zero, restart game
JNZ R0, ReturnFromCheckBottomBoundary		; If not at the bottom boundary, return from subroutine (with a non-zero value)

CheckBottomRestartGame:
INV R5, R5

ReturnFromCheckBottomBoundary:			
RET									; Return from subroutine
; =========================================================