# CAMERA_NOTE — Railway Time (10 s silent test)

Reasons the plan keeps WARNs on purpose:
- `speed median/p90 too calm`: the two travels in a 10-second film are short by nature; the gate's
  3-7 s flowing-move target is for films of 30 s or more. The loop return sweep (station 7)
  is the signature move and is kept as one calm 1.0 s sweep back to frame 0.
- `word station not at rest on its word` ([sun,2]): the loop station travels straight into the
  final frame on purpose (lead 0, no rest after), because the film must loop to frame 0.

Fixed this round: travel_roll 4 -> 2 (roll peak), "watch" added to the 'lies' station shows.
